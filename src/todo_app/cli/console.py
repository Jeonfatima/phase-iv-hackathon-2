"""
Console interface for the todo application.
"""
from typing import Optional
from ..services.task_service import TaskService
from ..models.task import Task


class ConsoleInterface:
    """
    Console interface for interacting with the todo application.
    """
    def __init__(self):
        self.task_service = TaskService()

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("TODO APPLICATION - MAIN MENU")
        print("="*50)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """Get user's menu choice."""
        try:
            choice = input("Enter your choice (1-6): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application...")
            return "6"  # Return exit option

    def add_task(self):
        """Add a new task."""
        print("\n--- ADD TASK ---")
        try:
            title = input("Enter task title: ").strip()

            if not title:
                print("Error: Title cannot be empty.")
                return

            if len(title) > 100:
                print("Error: Title must be 100 characters or less.")
                return

            description_input = input("Enter task description (optional, press Enter to skip): ").strip()
            description = description_input if description_input else None

            if description and len(description) > 500:
                print("Error: Description must be 500 characters or less.")
                return

            task = self.task_service.create_task(title, description)
            print(f"✓ Task added successfully with ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def view_tasks(self):
        """View all tasks."""
        print("\n--- ALL TASKS ---")
        try:
            tasks = self.task_service.get_all_tasks()

            if not tasks:
                print("No tasks found.")
                return

            print(f"{'ID':<4} {'Status':<10} {'Title':<20} {'Description':<30}")
            print("-" * 70)

            for task in tasks:
                status = "✓ Done" if task.completed else "○ Pending"
                title = task.title if len(task.title) <= 19 else task.title[:17] + ".."
                desc = task.description if task.description else ""
                if len(desc) > 29:
                    desc = desc[:27] + ".."
                print(f"{task.id:<4} {status:<10} {title:<20} {desc:<30}")
        except Exception as e:
            print(f"An error occurred while retrieving tasks: {e}")

    def update_task(self):
        """Update an existing task."""
        print("\n--- UPDATE TASK ---")
        try:
            task_id_str = input("Enter task ID to update: ").strip()

            if not task_id_str.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)

            # Check if task exists
            try:
                current_task = self.task_service.get_task_by_id(task_id)
            except ValueError as e:
                print(f"Error: {e}")
                return

            print(f"Current task: {current_task.title}")
            if current_task.description:
                print(f"Current description: {current_task.description}")

            new_title = input(f"Enter new title (current: '{current_task.title}', press Enter to keep current): ").strip()
            new_title = new_title if new_title else None

            if new_title:
                if len(new_title) > 100:
                    print("Error: Title must be 100 characters or less.")
                    return
                if not new_title.strip():
                    print("Error: Title cannot be empty or whitespace-only.")
                    return

            new_desc = input(f"Enter new description (current: '{current_task.description or 'None'}', press Enter to keep current): ").strip()
            new_desc = new_desc if new_desc != "" else None

            if new_desc and len(new_desc) > 500:
                print("Error: Description must be 500 characters or less.")
                return

            updated_task = self.task_service.update_task(task_id, new_title, new_desc)
            print(f"✓ Task updated successfully!")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete_task(self):
        """Delete a task."""
        print("\n--- DELETE TASK ---")
        try:
            task_id_str = input("Enter task ID to delete: ").strip()

            if not task_id_str.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)

            # Check if task exists
            try:
                current_task = self.task_service.get_task_by_id(task_id)
                print(f"Task to delete: {current_task.title}")
            except ValueError as e:
                print(f"Error: {e}")
                return

            confirm = input(f"Are you sure you want to delete task '{current_task.title}'? (y/N): ").strip().lower()

            if confirm in ['y', 'yes']:
                success = self.task_service.delete_task(task_id)
                if success:
                    print("✓ Task deleted successfully!")
                else:
                    print("Task was not found (this shouldn't happen).")
            else:
                print("Task deletion cancelled.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def toggle_task_completion(self):
        """Toggle task completion status."""
        print("\n--- TOGGLE TASK COMPLETION ---")
        try:
            task_id_str = input("Enter task ID to toggle completion: ").strip()

            if not task_id_str.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)

            # Check if task exists
            try:
                current_task = self.task_service.get_task_by_id(task_id)
            except ValueError as e:
                print(f"Error: {e}")
                return

            print(f"Current task: {current_task.title}")
            print(f"Current status: {'Completed' if current_task.completed else 'Incomplete'}")

            updated_task = self.task_service.toggle_task_completion(task_id)
            new_status = "Completed" if updated_task.completed else "Incomplete"
            print(f"✓ Task status updated to: {new_status}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Application!")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.toggle_task_completion()
            elif choice == "6":
                print("Thank you for using the Todo Application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

            # Pause to let user see the result before showing menu again
            if choice != "6":
                input("\nPress Enter to continue...")