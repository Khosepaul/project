from datetime import datetime, date

FILE_NAME = "tasks.txt"


def load_tasks():
    tasks = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 4:
                    continue

                text, done_str, due, priority = parts
                task = {
                    "text": text,
                    "done": (done_str == "True"),
                    "due": due,
                    "priority": priority
                }
                tasks.append(task)
    except FileNotFoundError:
        pass
    return tasks


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(f"{task['text']}|{task['done']}|{task['due']}|{task['priority']}\n")


def valid_date(date_text):
    if date_text == "":
        return "NONE"
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError:
        return None


def valid_priority(priority_text):
    priority_text = priority_text.strip().title()
    if priority_text in ["High", "Medium", "Low"]:
        return priority_text
    return None


def due_key(task):
    if task["due"] == "NONE":
        return date.max
    try:
        return datetime.strptime(task["due"], "%Y-%m-%d").date()
    except ValueError:
        return date.max


def priority_key(task):
    order = {"High": 1, "Medium": 2, "Low": 3}
    return order.get(task["priority"], 4)


def is_overdue(task):
    if task["done"] or task["due"] == "NONE":
        return False
    try:
        return datetime.strptime(task["due"], "%Y-%m-%d").date() < date.today()
    except ValueError:
        return False


def display_tasks(view):
    if not view:
        print("\nNo tasks found.")
        return

    print("\n" + "=" * 60)
    print("YOUR TASKS")
    print("=" * 60)

    for i, task in enumerate(view, start=1):
        status = "Complete" if task["done"] else "Incomplete"
        due_display = task["due"] if task["due"] != "NONE" else "No due date"
        overdue_tag = " [OVERDUE]" if is_overdue(task) else ""

        print(f"{i}. {task['text']}")
        print(f"   Status: {status}")
        print(f"   Due: {due_display}")
        print(f"   Priority: {task['priority']}{overdue_tag}")
        print("-" * 60)


def get_view(tasks, mode="all"):
    view = tasks[:]

    if mode == "all_sorted":
        view.sort(key=lambda t: (due_key(t), priority_key(t)))
    elif mode == "incomplete_sorted":
        view = [t for t in view if not t["done"]]
        view.sort(key=lambda t: (due_key(t), priority_key(t)))
    elif mode == "overdue_sorted":
        view = [t for t in view if is_overdue(t)]
        view.sort(key=lambda t: (due_key(t), priority_key(t)))
    elif mode == "high_priority":
        view = [t for t in view if t["priority"] == "High"]
        view.sort(key=lambda t: (due_key(t), priority_key(t)))

    return view


def choose_task_from_view(tasks, mode="all"):
    view = get_view(tasks, mode)
    if not view:
        print("\nNo tasks match that view.")
        return None

    display_tasks(view)

    try:
        num = int(input("Enter task number: "))
        if 1 <= num <= len(view):
            return view[num - 1]
        else:
            print("Invalid task number.")
            return None
    except ValueError:
        print("Please enter a number.")
        return None


def add_task(tasks):
    print("\nADD TASK")
    text = input("Enter task name: ").strip()
    if not text:
        print("Task cannot be empty.")
        return

    while True:
        due_input = input("Enter due date (YYYY-MM-DD) or press Enter for none: ").strip()
        due = valid_date(due_input)
        if due is not None:
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    while True:
        priority_input = input("Enter priority (High/Medium/Low): ").strip()
        priority = valid_priority(priority_input)
        if priority is not None:
            break
        print("Invalid priority. Please enter High, Medium, or Low.")

    task = {
        "text": text,
        "done": False,
        "due": due,
        "priority": priority
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully.")


def delete_task(tasks):
    print("\nDELETE TASK")
    task = choose_task_from_view(tasks, "all_sorted")
    if task is None:
        return

    tasks.remove(task)
    save_tasks(tasks)
    print(f"Deleted task: {task['text']}")


def toggle_task(tasks):
    print("\nTOGGLE COMPLETE/INCOMPLETE")
    task = choose_task_from_view(tasks, "all_sorted")
    if task is None:
        return

    task["done"] = not task["done"]
    save_tasks(tasks)
    print("Task status updated.")


def edit_due_date(tasks):
    print("\nEDIT DUE DATE")
    task = choose_task_from_view(tasks, "all_sorted")
    if task is None:
        return

    while True:
        due_input = input("Enter new due date (YYYY-MM-DD) or press Enter for none: ").strip()
        due = valid_date(due_input)
        if due is not None:
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    task["due"] = due
    save_tasks(tasks)
    print("Due date updated.")


def edit_task_name(tasks):
    print("\nEDIT TASK NAME")
    task = choose_task_from_view(tasks, "all_sorted")
    if task is None:
        return

    new_text = input("Enter new task name: ").strip()
    if not new_text:
        print("Task name cannot be empty.")
        return

    task["text"] = new_text
    save_tasks(tasks)
    print("Task name updated.")


def edit_priority(tasks):
    print("\nEDIT PRIORITY")
    task = choose_task_from_view(tasks, "all_sorted")
    if task is None:
        return

    while True:
        priority_input = input("Enter new priority (High/Medium/Low): ").strip()
        priority = valid_priority(priority_input)
        if priority is not None:
            break
        print("Invalid priority. Please enter High, Medium, or Low.")

    task["priority"] = priority
    save_tasks(tasks)
    print("Priority updated.")


def search_tasks(tasks):
    print("\nSEARCH TASKS")
    keyword = input("Enter keyword to search: ").strip().lower()
    if not keyword:
        print("Search cannot be empty.")
        return

    results = [task for task in tasks if keyword in task["text"].lower()]

    if not results:
        print("No matching tasks found.")
    else:
        display_tasks(results)


def show_stats(tasks):
    total = len(tasks)
    completed = sum(1 for task in tasks if task["done"])
    incomplete = total - completed
    overdue = sum(1 for task in tasks if is_overdue(task))
    high_priority = sum(1 for task in tasks if task["priority"] == "High")

    print("\n" + "=" * 40)
    print("TASK STATISTICS")
    print("=" * 40)
    print(f"Total tasks: {total}")
    print(f"Completed tasks: {completed}")
    print(f"Incomplete tasks: {incomplete}")
    print(f"Overdue tasks: {overdue}")
    print(f"High priority tasks: {high_priority}")

    if total > 0:
        percent_complete = (completed / total) * 100
        print(f"Percent complete: {percent_complete:.1f}%")
    print("=" * 40)


def show_menu():
    print("\n" + "=" * 40)
    print("TASK TRACKER MENU")
    print("=" * 40)
    print("1. View all tasks")
    print("2. View all tasks (sorted)")
    print("3. View incomplete tasks")
    print("4. View overdue tasks")
    print("5. View high priority tasks")
    print("6. Add task")
    print("7. Delete task")
    print("8. Toggle complete/incomplete")
    print("9. Edit due date")
    print("10. Edit task name")
    print("11. Edit priority")
    print("12. Search tasks")
    print("13. Show statistics")
    print("14. Quit")


def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-14): ").strip()

        if choice == "1":
            display_tasks(get_view(tasks, "all"))
        elif choice == "2":
            display_tasks(get_view(tasks, "all_sorted"))
        elif choice == "3":
            display_tasks(get_view(tasks, "incomplete_sorted"))
        elif choice == "4":
            display_tasks(get_view(tasks, "overdue_sorted"))
        elif choice == "5":
            display_tasks(get_view(tasks, "high_priority"))
        elif choice == "6":
            add_task(tasks)
        elif choice == "7":
            delete_task(tasks)
        elif choice == "8":
            toggle_task(tasks)
        elif choice == "9":
            edit_due_date(tasks)
        elif choice == "10":
            edit_task_name(tasks)
        elif choice == "11":
            edit_priority(tasks)
        elif choice == "12":
            search_tasks(tasks)
        elif choice == "13":
            show_stats(tasks)
        elif choice == "14":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


main()
