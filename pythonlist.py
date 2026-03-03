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
                if len(parts) != 3:
                    continue
                text, done_str, due = parts
                done = (done_str == "True")
                tasks.append([text, done, due])
    except FileNotFoundError:
        pass
    return tasks

def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        for t in tasks:
            file.write(f"{t[0]}|{t[1]}|{t[2]}\n")

def due_key(t):
    if t[2] == "NONE":
        return date.max
    try:
        return datetime.strptime(t[2], "%Y-%m-%d").date()
    except ValueError:
        return date.max

def is_overdue(t):
    if t[1] or t[2] == "NONE":
        return False
    try:
        return datetime.strptime(t[2], "%Y-%m-%d").date() < date.today()
    except ValueError:
        return False

def show_tasks(tasks, mode="all"):
    if not tasks:
        print("\nNo tasks found.")
        return

    view = tasks[:]

    if mode in ("all_sorted", "incomplete_sorted", "overdue_sorted"):
        view.sort(key=due_key)

    if mode == "incomplete_sorted":
        view = [t for t in view if not t[1]]
    elif mode == "overdue_sorted":
        view = [t for t in view if is_overdue(t)]

    if not view:
        print("\nNo tasks match that view.")
        return

    print("\nYour Tasks:")
    for i, t in enumerate(view, start=1):
        status = "Complete" if t[1] else "Incomplete"
        due_display = t[2] if t[2] != "NONE" else "No due date"
        tag = " [OVERDUE]" if is_overdue(t) else ""
        print(f"{i}. {t[0]} ({status}, Due: {due_display}){tag}")

def add_task(tasks):
    text = input("Enter a new task: ").strip()
    if not text:
        print("Task cannot be empty.")
        return

    due = input("Enter due date (YYYY-MM-DD) or press Enter for none: ").strip()
    if due == "":
        due = "NONE"

    tasks.append([text, False, due])
    save_tasks(tasks)
    print("Task added.")

def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks(tasks)
            print(f"Deleted task: {removed[0]}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a number.")

def toggle_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to toggle complete/incomplete: "))
        if 1 <= num <= len(tasks):
            tasks[num - 1][1] = not tasks[num - 1][1]
            save_tasks(tasks)
            print("Task updated.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a number.")

def edit_due_date(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to change due date: "))
        if 1 <= num <= len(tasks):
            due = input("Enter new due date (YYYY-MM-DD) or press Enter for none: ").strip()
            tasks[num - 1][2] = "NONE" if due == "" else due
            save_tasks(tasks)
            print("Due date updated.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a number.")

def main():
    tasks = load_tasks()

    while True:
        print("\nTask Tracker Menu")
        print("1. View tasks (all)")
        print("2. View tasks (sorted by due date)")
        print("3. View incomplete only (sorted)")
        print("4. View overdue only (sorted)")
        print("5. Add task")
        print("6. Delete task")
        print("7. Toggle complete/incomplete")
        print("8. Edit due date")
        print("9. Quit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            show_tasks(tasks, "all")
        elif choice == "2":
            show_tasks(tasks, "all_sorted")
        elif choice == "3":
            show_tasks(tasks, "incomplete_sorted")
        elif choice == "4":
            show_tasks(tasks, "overdue_sorted")
        elif choice == "5":
            add_task(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            toggle_task(tasks)
        elif choice == "8":
            edit_due_date(tasks)
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

main()
