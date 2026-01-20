"""
Test to demonstrate the command interpretation issue in AI service
"""

from services.ai_service import AIService


def test_command_interpretation_issues():
    """Test to show the issues with command interpretation"""

    print("Testing command interpretation issues...")

    # Issue 1: Delete command interpreted as add command
    delete_result = AIService._interpret_message_manually("Delete task 5")
    print(f"Delete command 'Delete task 5' result: {delete_result}")
    print(f"Expected: delete_task tool call, Got: {delete_result.get('tool_calls', [])}")

    # Issue 2: List command might have similar issues
    list_result = AIService._interpret_message_manually("Show my tasks")
    print(f"List command 'Show my tasks' result: {list_result}")
    print(f"Got tool call: {list_result.get('tool_calls', [])}")

    # Issue 3: Update command not recognized
    update_result = AIService._interpret_message_manually("Update task 1 title to new title")
    print(f"Update command 'Update task 1 title to new title' result: {update_result}")
    print(f"Expected: update_task tool call, Got: {update_result.get('tool_calls', [])}")

    # Issue 4: Another delete example
    delete_result2 = AIService._interpret_message_manually("Remove task 3")
    print(f"Delete command 'Remove task 3' result: {delete_result2}")
    print(f"Expected: delete_task tool call, Got: {delete_result2.get('tool_calls', [])}")

    print("\nThe issue is in the order of conditions in _interpret_message_manually:")
    print("- Lines 114 checks for ['add', 'create', 'new', 'task'] BEFORE")
    print("- Line 141 checks for ['delete', 'remove']")
    print("- Since 'delete task 5' contains 'task', it matches the first condition")
    print("- Also, there's no pattern for 'update' commands")


if __name__ == "__main__":
    test_command_interpretation_issues()