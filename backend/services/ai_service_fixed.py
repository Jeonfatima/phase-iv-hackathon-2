"""
Fixed version of the AI service with corrected command interpretation logic
"""

import os
from typing import Dict, Any, List, Optional
import cohere
from dotenv import load_dotenv
from .mcp_tools import (
    add_task, delete_task, update_task,
    complete_task, list_tasks, get_current_user
)
import re


class FixedAIService:
    """
    Fixed version of AIService with corrected command interpretation
    """

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
            task_id_match = re.search(r'task\s+(\d+)|(\d+)\s+task', user_message, re.IGNORECASE)

            # Extract title and description if mentioned
            title_match = re.search(r'(?:title|to)\s+(.+?)(?:\s|$)|"([^"]+)"', user_message, re.IGNORECASE)
            desc_match = re.search(r'(?:description|desc|details?)\s+(.+?)(?:\s|$)|"([^"]+)"', user_message, re.IGNORECASE)

            if task_id_match:
                task_id_str = task_id_match.group(1) or task_id_match.group(2)
                if task_id_str:
                    task_id = int(task_id_str)

                    update_args = {"task_id": task_id}

                    if title_match:
                        title = title_match.group(1) or title_match.group(2)
                        if title:
                            update_args["title"] = title.strip()

                    if desc_match:
                        desc = desc_match.group(1) or desc_match.group(2)
                        if desc:
                            update_args["description"] = desc.strip()

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


# Test the fixed version
if __name__ == "__main__":
    print("Testing FIXED command interpretation...")
    print()

    test_commands = [
        "Delete task 5",
        "Remove task 3",
        "Update task 1 title to new title",
        "Change task 2 description to updated description",
        "Show my tasks",
        "List completed tasks",
        "Add a task to buy groceries",
        "Create task to call mom"
    ]

    for cmd in test_commands:
        result = FixedAIService._interpret_message_manually(cmd)
        tool_calls = result.get("tool_calls", [])
        tool_names = [tc["name"] for tc in tool_calls] if tool_calls else ["none"]
        print(f"'{cmd}' -> {tool_names}")