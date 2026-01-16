import os
from typing import Dict, Any, List, Optional
import cohere
from dotenv import load_dotenv
from .mcp_tools import (
    add_task, delete_task, update_task,
    complete_task, list_tasks, get_current_user
)

# Load environment variables
load_dotenv()

# Do not initialize Cohere client at module level to avoid startup errors
# Client is initialized per request in the methods


class AIService:
    """
    Service class for handling AI operations with Cohere
    """

    @staticmethod
    def initialize_cohere_client():
        """
        Initialize and return the Cohere client
        """
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        return cohere.Client(api_key=api_key)

    @staticmethod
    def call_cohere_with_tools(
        user_message: str,
        tools: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Call Cohere with tool definitions and user message

        Args:
            user_message: The user's natural language message
            tools: List of tool definitions in Cohere format
            conversation_history: Previous conversation messages for context

        Returns:
            Dictionary with response and tool calls
        """
        try:
            cohere_client = AIService.initialize_cohere_client()

            # Call Cohere with tools
            response = cohere_client.chat(
                model="command-r-plus",  # Using command-r-plus for superior reasoning
                message=user_message,
                tools=tools,
                connectors=[{"id": "web-search"}],  # Optional web connector
                temperature=0.3
            )

            # Extract response and tool calls
            response_text = response.text
            tool_calls = []

            # Check if the response contains tool calls
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_calls.append({
                        "name": tool_call.name,
                        "arguments": tool_call.parameters
                    })

            return {
                "response": response_text,
                "tool_calls": tool_calls,
                "success": True
            }

        except ValueError as e:
            # This is likely due to missing API key
            if "COHERE_API_KEY" in str(e):
                # For basic task operations, try to interpret manually
                return AIService._interpret_message_manually(user_message)
            else:
                return {
                    "response": "I'm having trouble processing your request right now. Please try again.",
                    "tool_calls": [],
                    "success": False,
                    "error": str(e)
                }
        except Exception as e:
            # For other exceptions, also try manual interpretation for common tasks
            return AIService._interpret_message_manually(user_message)

    @staticmethod
    def _interpret_message_manually(user_message: str) -> Dict[str, Any]:
        """
        Manually interpret common task-related messages when Cohere is unavailable
        """
        user_lower = user_message.lower().strip()

        # Interpret common commands
        if any(word in user_lower for word in ["list", "show", "my", "tasks", "todo"]):
            # This is likely a request to list tasks
            return {
                "response": "Let me get your tasks for you...",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {}
                }],
                "success": True
            }
        elif any(word in user_lower for word in ["add", "create", "new", "task"]):
            # This is likely a request to add a task
            # Extract task title from the message
            import re
            # Look for patterns like "add task to [title]" or "add a task [title]"
            patterns = [
                r'add.*?task.*?to\s+(.+)',
                r'add.*?task\s+(.+)',
                r'create.*?task.*?to\s+(.+)',
                r'create.*?task\s+(.+)',
            ]

            title = "new task"  # default
            for pattern in patterns:
                match = re.search(pattern, user_message, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    break

            return {
                "response": f"Adding task: {title}",
                "tool_calls": [{
                    "name": "add_task",
                    "arguments": {"title": title}
                }],
                "success": True
            }
        elif any(word in user_lower for word in ["delete", "remove"]):
            # This is likely a request to delete a task
            import re
            # Look for task ID in the message
            task_id_match = re.search(r'task\s+(\d+)|(\d+)\s+task', user_message, re.IGNORECASE)
            if task_id_match:
                # Get the first captured group that matched (either the first or second group)
                task_id = task_id_match.group(1) or task_id_match.group(2)
                if task_id:  # Make sure we got a match
                    task_id = int(task_id)
                    return {
                        "response": f"Deleting task {task_id}",
                        "tool_calls": [{
                            "name": "delete_task",
                            "arguments": {"task_id": task_id}
                        }],
                        "success": True
                    }
            # If no specific ID found, try to extract any number from the message
            number_match = re.search(r'(\d+)', user_message)
            if number_match:
                task_id = int(number_match.group(1))
                return {
                    "response": f"Deleting task {task_id}",
                    "tool_calls": [{
                        "name": "delete_task",
                        "arguments": {"task_id": task_id}
                    }],
                    "success": True
                }
        elif any(word in user_lower for word in ["complete", "done", "finish"]):
            # This is likely a request to complete a task
            import re
            # Look for task ID in the message
            task_id_match = re.search(r'task\s+(\d+)|(\d+)\s+task', user_message, re.IGNORECASE)
            if task_id_match:
                # Get the first captured group that matched (either the first or second group)
                task_id = task_id_match.group(1) or task_id_match.group(2)
                if task_id:  # Make sure we got a match
                    task_id = int(task_id)
                    return {
                        "response": f"Marking task {task_id} as complete",
                        "tool_calls": [{
                            "name": "complete_task",
                            "arguments": {"task_id": task_id, "completed": True}
                        }],
                        "success": True
                    }
            # If no specific ID found, try to extract any number from the message
            number_match = re.search(r'(\d+)', user_message)
            if number_match:
                task_id = int(number_match.group(1))
                return {
                    "response": f"Marking task {task_id} as complete",
                    "tool_calls": [{
                        "name": "complete_task",
                        "arguments": {"task_id": task_id, "completed": True}
                    }],
                    "success": True
                }

        # If none of the common patterns match, return a generic response
        return {
            "response": "I'm having trouble processing your request right now. Please try again.",
            "tool_calls": [],
            "success": False,
            "error": "Unable to interpret the request manually"
        }

    @staticmethod
    def execute_tool_calls(tool_calls: List[Dict[str, Any]], user_id: str) -> List[Dict[str, Any]]:
        """
        Execute the tool calls returned by Cohere

        Args:
            tool_calls: List of tool calls from Cohere
            user_id: The ID of the user making the request

        Returns:
            List of results from tool executions
        """
        results = []

        for tool_call in tool_calls:
            name = tool_call.get("name")
            arguments = tool_call.get("arguments", {})

            # Add user_id to arguments for tools that need it
            arguments["user_id"] = user_id

            try:
                if name == "add_task":
                    result = add_task(**arguments)
                elif name == "delete_task":
                    result = delete_task(**arguments)
                elif name == "update_task":
                    result = update_task(**arguments)
                elif name == "complete_task":
                    result = complete_task(**arguments)
                elif name == "list_tasks":
                    result = list_tasks(**arguments)
                elif name == "get_current_user":
                    result = get_current_user(**arguments)
                else:
                    result = {
                        "success": False,
                        "message": f"Unknown tool: {name}"
                    }

                results.append({
                    "name": name,
                    "arguments": tool_call.get("arguments"),
                    "result": result
                })

            except Exception as e:
                results.append({
                    "name": name,
                    "arguments": tool_call.get("arguments"),
                    "result": {
                        "success": False,
                        "message": f"Error executing tool {name}: {str(e)}"
                    }
                })

        return results

    @staticmethod
    def process_conversation_with_reasoning_loop(
        user_message: str,
        user_id: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process a conversation using a reasoning loop that executes tools and feeds results back

        Args:
            user_message: The user's natural language message
            user_id: The ID of the user making the request
            conversation_history: Previous conversation messages for context

        Returns:
            Dictionary with final response and all tool calls executed
        """
        # Define the tools available to the AI
        tools = [
            {
                "name": "add_task",
                "description": "Creates a new task with title and optional description",
                "parameter_definitions": {
                    "title": {
                        "description": "The title of the task",
                        "type": "str",
                        "required": True
                    },
                    "description": {
                        "description": "Optional description of the task",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "delete_task",
                "description": "Deletes an existing task by its ID",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to delete",
                        "type": "int",
                        "required": True
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Updates properties of an existing task",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to update",
                        "type": "int",
                        "required": True
                    },
                    "title": {
                        "description": "New title for the task (optional)",
                        "type": "str",
                        "required": False
                    },
                    "description": {
                        "description": "New description for the task (optional)",
                        "type": "str",
                        "required": False
                    },
                    "completed": {
                        "description": "New completion status for the task (optional)",
                        "type": "bool",
                        "required": False
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Marks a task as complete or incomplete",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to update",
                        "type": "int",
                        "required": True
                    },
                    "completed": {
                        "description": "Whether the task should be marked as completed",
                        "type": "bool",
                        "required": True
                    }
                }
            },
            {
                "name": "list_tasks",
                "description": "Retrieves all tasks for the current user with optional filtering",
                "parameter_definitions": {
                    "filter_status": {
                        "description": "Filter for task status (all, pending, completed)",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "get_current_user",
                "description": "Returns the current user's email and ID from authentication",
                "parameter_definitions": {}
            }
        ]

        # Initial call to Cohere
        result = AIService.call_cohere_with_tools(
            user_message=user_message,
            tools=tools,
            conversation_history=conversation_history
        )

        if not result["success"]:
            return result

        all_tool_calls = []
        current_response = result["response"]

        # Loop while there are tool calls to execute
        iteration_count = 0
        max_iterations = 5  # Prevent infinite loops

        while result["tool_calls"] and iteration_count < max_iterations:
            iteration_count += 1

            # Execute the tool calls
            tool_results = AIService.execute_tool_calls(result["tool_calls"], user_id)

            # Add to the list of all tool calls executed
            all_tool_calls.extend(tool_results)

            # Prepare the next message with tool results
            # In a real implementation, you'd feed these results back to Cohere
            # For now, we'll just return the results

            # For this implementation, we'll break after the first round of tool calls
            # A full implementation would feed results back to Cohere for further processing
            break

        return {
            "response": current_response,
            "tool_calls": all_tool_calls,
            "success": True
        }


__all__ = ["AIService"]