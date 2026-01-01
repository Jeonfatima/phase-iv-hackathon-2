"""
Integration tests for the CLI interface.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.todo_app.cli.console import ConsoleInterface


class TestCLIIntegration:
    """Integration tests for the CLI interface."""

    def test_add_task_integration(self):
        """Test adding a task through the CLI interface."""
        console = ConsoleInterface()

        # Mock user input for title and description
        with patch('builtins.input', side_effect=['Test Task', 'Test Description']):
            with patch('builtins.print') as mock_print:
                console.add_task()

                # Verify the task was added successfully
                tasks = console.task_service.get_all_tasks()
                assert len(tasks) == 1
                assert tasks[0].title == "Test Task"
                assert tasks[0].description == "Test Description"
                assert tasks[0].completed is False

    def test_view_tasks_integration(self):
        """Test viewing tasks through the CLI interface."""
        console = ConsoleInterface()

        # Add a task first
        console.task_service.create_task("Test Task", "Test Description")

        with patch('builtins.print') as mock_print:
            console.view_tasks()

            # Verify that print was called (meaning tasks were displayed)
            assert mock_print.called

    def test_update_task_integration(self):
        """Test updating a task through the CLI interface."""
        console = ConsoleInterface()

        # Add a task first
        task = console.task_service.create_task("Original Task", "Original Description")

        # Mock user input for update
        with patch('builtins.input', side_effect=[str(task.id), "Updated Task", "Updated Description"]):
            with patch('builtins.print') as mock_print:
                console.update_task()

                # Verify the task was updated
                updated_task = console.task_service.get_task_by_id(task.id)
                assert updated_task.title == "Updated Task"
                assert updated_task.description == "Updated Description"

    def test_delete_task_integration(self):
        """Test deleting a task through the CLI interface."""
        console = ConsoleInterface()

        # Add a task first
        task = console.task_service.create_task("Test Task", "Test Description")

        # Verify task exists
        tasks = console.task_service.get_all_tasks()
        assert len(tasks) == 1

        # Mock user input for deletion confirmation
        with patch('builtins.input', side_effect=[str(task.id), 'y']):
            with patch('builtins.print') as mock_print:
                console.delete_task()

                # Verify the task was deleted
                tasks = console.task_service.get_all_tasks()
                assert len(tasks) == 0

    def test_toggle_task_completion_integration(self):
        """Test toggling task completion through the CLI interface."""
        console = ConsoleInterface()

        # Add a task first
        task = console.task_service.create_task("Test Task", "Test Description")

        # Initially should be incomplete
        assert task.completed is False

        # Mock user input for toggling
        with patch('builtins.input', side_effect=[str(task.id)]):
            with patch('builtins.print') as mock_print:
                console.toggle_task_completion()

                # Verify the task completion was toggled
                toggled_task = console.task_service.get_task_by_id(task.id)
                assert toggled_task.completed is True

    def test_main_menu_flow(self):
        """Test the main menu flow with different choices."""
        console = ConsoleInterface()

        # Add a test task
        console.task_service.create_task("Test Task", "Test Description")

        # Mock user choices and inputs - need to handle the "Press Enter to continue..." prompt
        inputs = ['2', '', '6', '']  # View tasks, press enter, exit, press enter

        def mock_input(prompt=""):
            return inputs.pop(0)

        with patch('builtins.input', side_effect=mock_input):
            with patch('builtins.print'):
                console.run()  # This will execute the menu loop

    def test_error_handling_for_invalid_task_id(self):
        """Test error handling when using an invalid task ID."""
        console = ConsoleInterface()

        # Mock user input for an invalid task ID
        with patch('builtins.input', side_effect=['999']):
            with patch('builtins.print') as mock_print:
                console.update_task()

                # Verify an error message was printed
                error_printed = any("Error:" in str(call) for call in mock_print.call_args_list)
                assert error_printed