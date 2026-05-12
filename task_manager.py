import json
import os
import argparse
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

FILE_NAME = "tasks.json"


# -----------------------------
# LOAD TASKS
# -----------------------------
def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


# -----------------------------
# SAVE TASKS
# -----------------------------
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


# -----------------------------
# VIEW TASKS
# -----------------------------
def view_tasks(tasks):

    if not tasks:
        print(Fore.YELLOW + "No tasks available.")
        return

    print("\n====== TASK LIST ======\n")

    for i, task in enumerate(tasks):

        status = "✓" if task["done"] else "✗"

        color = Fore.GREEN if task["done"] else Fore.RED

        print(
            color
            + f"{i+1}. {task['title']} "
              f"[{status}] "
              f"| Priority: {task['priority']} "
              f"| Due: {task['due_date']}"
        )

    print()


# -----------------------------
# SEARCH TASKS
# -----------------------------
def search_tasks(tasks, keyword):

    keyword = keyword.lower()

    found = False

    print("\n====== SEARCH RESULTS ======\n")

    for i, task in enumerate(tasks):

        if keyword in task["title"].lower():

            found = True

            status = "✓" if task["done"] else "✗"

            print(
                f"{i+1}. {task['title']} "
                f"[{status}] "
                f"| Priority: {task['priority']} "
                f"| Due: {task['due_date']}"
            )

    if not found:
        print(Fore.YELLOW + "No matching tasks found.")

    print()


# -----------------------------
# SORT TASKS
# -----------------------------
def sort_tasks(tasks):

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    tasks.sort(
        key=lambda task: (
            task["done"],
            priority_order.get(task["priority"], 4)
        )
    )

    save_tasks(tasks)

    print(Fore.GREEN + "Tasks sorted successfully!")


# -----------------------------
# UPDATE TASK
# -----------------------------
def update_task(tasks, task_no, new_title):

    if 1 <= task_no <= len(tasks):

        old_title = tasks[task_no - 1]["title"]

        tasks[task_no - 1]["title"] = new_title

        save_tasks(tasks)

        print(
            Fore.GREEN
            + f"Updated task '{old_title}' -> '{new_title}'"
        )

    else:
        print(Fore.RED + "Invalid task number.")


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():

    tasks = load_tasks()

    parser = argparse.ArgumentParser(
        description="CLI Task Manager"
    )

    subparsers = parser.add_subparsers(dest="command")

    # -------------------------
    # ADD COMMAND
    # -------------------------
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new task"
    )

    add_parser.add_argument(
        "title",
        help="Task title"
    )

    add_parser.add_argument(
        "--priority",
        default="Medium",
        choices=["High", "Medium", "Low"],
        help="Task priority"
    )

    add_parser.add_argument(
        "--due",
        default="No due date",
        help="Due date"
    )

    # -------------------------
    # LIST COMMAND
    # -------------------------
    subparsers.add_parser(
        "list",
        help="View all tasks"
    )

    # -------------------------
    # COMPLETE COMMAND
    # -------------------------
    complete_parser = subparsers.add_parser(
        "complete",
        help="Mark task as complete"
    )

    complete_parser.add_argument(
        "task_number",
        type=int,
        help="Task number"
    )

    # -------------------------
    # DELETE COMMAND
    # -------------------------
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task"
    )

    delete_parser.add_argument(
        "task_number",
        type=int,
        help="Task number"
    )

    # -------------------------
    # SEARCH COMMAND
    # -------------------------
    search_parser = subparsers.add_parser(
        "search",
        help="Search tasks"
    )

    search_parser.add_argument(
        "keyword",
        help="Keyword to search"
    )

    # -------------------------
    # SORT COMMAND
    # -------------------------
    subparsers.add_parser(
        "sort",
        help="Sort tasks"
    )

    # -------------------------
    # UPDATE COMMAND
    # -------------------------
    update_parser = subparsers.add_parser(
        "update",
        help="Update task title"
    )

    update_parser.add_argument(
        "task_number",
        type=int,
        help="Task number"
    )

    update_parser.add_argument(
        "new_title",
        help="New task title"
    )

    args = parser.parse_args()

    # -------------------------
    # HANDLE COMMANDS
    # -------------------------

    if args.command == "add":

        new_task = {
            "title": args.title,
            "done": False,
            "priority": args.priority,
            "due_date": args.due
        }

        tasks.append(new_task)

        save_tasks(tasks)

        print(Fore.GREEN + "Task added successfully!")

    elif args.command == "list":

        view_tasks(tasks)

    elif args.command == "complete":

        task_no = args.task_number

        if 1 <= task_no <= len(tasks):

            tasks[task_no - 1]["done"] = True

            save_tasks(tasks)

            print(Fore.GREEN + "Task marked as complete!")

        else:
            print(Fore.RED + "Invalid task number.")

    elif args.command == "delete":

        task_no = args.task_number

        if 1 <= task_no <= len(tasks):

            removed_task = tasks.pop(task_no - 1)

            save_tasks(tasks)

            print(
                Fore.GREEN
                + f"Deleted task: {removed_task['title']}"
            )

        else:
            print(Fore.RED + "Invalid task number.")

    elif args.command == "search":

        search_tasks(tasks, args.keyword)

    elif args.command == "sort":

        sort_tasks(tasks)

    elif args.command == "update":

        update_task(
            tasks,
            args.task_number,
            args.new_title
        )

    else:
        parser.print_help()


# -----------------------------
# RUN PROGRAM
# -----------------------------
if __name__ == "__main__":
    main()