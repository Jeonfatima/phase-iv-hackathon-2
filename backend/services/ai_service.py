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
        FIXED VERSION: Corrected the order and added missing patterns
        """
        user_lower = user_message.lower().strip()

        # Check for specific commands FIRST, before general terms

        # UPDATE TASKS - Check for update/modify/change commands first
        if any(word in user_lower for word in ["update", "modify", "change", "edit"]):
            # This is likely a request to update a task
            # Look for task ID and what to update
            import re
            task_id_match = re.search(r'task\s+(\d+)|(\d+)\s+task', user_message, re.IGNORECASE)

            # Extract title and description if mentioned - improved regex
            # Look for patterns like "update task 1 title to NEW_TITLE" or "update task 1 to NEW_TITLE"
            title_match = None
            # First try to match "title to ..." or "description to ..."
            title_to_match = re.search(r'(?:title|name)\s+to\s+(.+?)(?:\s+(?:and|description|desc)\s+|\s*$)', user_message, re.IGNORECASE)
            if not title_to_match:
                # Try "update task X to ..." pattern
                title_to_match = re.search(r'to\s+(.+?)(?:\s+(?:and|description|desc)\s+|\s*$)', user_message, re.IGNORECASE)

            # Look for description pattern
            desc_match = re.search(r'(?:description|desc|details?)\s+(?:to\s+)?(.+?)(?:\s+(?:and|title|name)\s+|\s*$)', user_message, re.IGNORECASE)

            if task_id_match:
                task_id_str = task_id_match.group(1) or task_id_match.group(2)
                if task_id_str:
                    task_id = int(task_id_str)

                    update_args = {"task_id": task_id}

                    if title_to_match:
                        title = title_to_match.group(1).strip()
                        if title and title.lower() != 'to':  # Avoid catching just the word 'to'
                            update_args["title"] = title

                    if desc_match:
                        desc = desc_match.group(1).strip()
                        if desc:
                            update_args["description"] = desc

                    if len(update_args) > 1:  # Has task_id plus at least one other field
                        return {
                            "response": f"Updating task {task_id}",
                            "tool_calls": [{
                                "name": "update_task",
                                "arguments": update_args
                            }],
                            "success": True
                        }

        # DELETE TASKS - Check for delete/remove commands before general terms
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

        # COMPLETE/FINISH TASKS
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

        # LIST TASKS
        elif any(word in user_lower for word in ["list", "show", "my", "tasks", "todo"]):
            # This is likely a request to list tasks
            # Check if there are filters like "pending", "completed", "all"
            if any(word in user_lower for word in ["pending", "incomplete", "not done"]):
                filter_status = "pending"
            elif any(word in user_lower for word in ["completed", "done", "finished"]):
                filter_status = "completed"
            else:
                filter_status = "all"  # default

            return {
                "response": "Let me get your tasks for you...",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {"filter_status": filter_status}
                }],
                "success": True
            }

        # ADD TASKS - Check for add commands LAST, after more specific ones
        elif any(word in user_lower for word in ["add", "create", "new"]):
            # This is likely a request to add a task
            import re
            # Extract task title from the message
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

        # Check if there are tool calls to execute
        if result["tool_calls"]:
            # Execute the tool calls
            tool_results = AIService.execute_tool_calls(result["tool_calls"], user_id)

            # Add to the list of all tool calls executed
            all_tool_calls.extend(tool_results)

            # Build the final response based on tool results
            final_response_parts = []

            for tool_result in tool_results:
                name = tool_result["name"]
                result_data = tool_result["result"]

                # Format the response based on the tool type and result
                if name == "list_tasks":
                    if result_data.get("success"):
                        tasks = result_data.get("tasks", [])
                        if tasks:
                            task_list = "\n".join([f"- {task['id']}. {task['title']} ({'✓' if task['completed'] else '○'})" for task in tasks])
                            final_response_parts.append(f"Here are your tasks:\n{task_list}")
                        else:
                            final_response_parts.append("You don't have any tasks right now.")
                    else:
                        final_response_parts.append("I couldn't retrieve your tasks. Please try again.")

                elif name == "add_task":
                    if result_data.get("success"):
                        task = result_data.get("task", {})
                        final_response_parts.append(f"I've added the task: '{task.get('title', 'Untitled')}'")
                    else:
                        final_response_parts.append("I couldn't add the task. Please try again.")

                elif name == "delete_task":
                    if result_data.get("success"):
                        final_response_parts.append("Task deleted successfully!")
                    else:
                        final_response_parts.append("I couldn't delete the task. Please check the task ID and try again.")

                elif name == "update_task":
                    if result_data.get("success"):
                        final_response_parts.append("Task updated successfully!")
                    else:
                        final_response_parts.append("I couldn't update the task. Please check the task ID and try again.")

                elif name == "complete_task":
                    if result_data.get("success"):
                        completed = result_data.get("task", {}).get("completed", False)
                        status = "completed" if completed else "marked as not completed"
                        final_response_parts.append(f"Task {status} successfully!")
                    else:
                        final_response_parts.append("I couldn't update the task status. Please check the task ID and try again.")

                elif name == "get_current_user":
                    if result_data.get("success"):
                        user_email = result_data.get("user", {}).get("email", "Unknown")
                        final_response_parts.append(f"You are logged in as: {user_email}")
                    else:
                        final_response_parts.append("I couldn't get your user information.")

            # Combine all parts into the final response
            current_response = " ".join(final_response_parts)

        return {
            "response": current_response,
            "tool_calls": all_tool_calls,
            "success": True
        }


__all__ = ["AIService"]