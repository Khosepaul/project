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
        for task in tasks:
            file.write(f"{task[0]}|{task[1]}|{task[2]}\n")


def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\nYour Tasks:")
    for i, task in enumerate(tasks, start=1):
        status = "Complete" if task[1] else "Incomplete"
        due_display = task[2] if task[2] != "NONE" else "No due date"
        print(f"{i}. {task[0]} ({status}, Due: {due_display})")


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
        print("1. View tasks")
        print("2. Add task")
        print("3. Delete task")
        print("4. Toggle complete/incomplete")
        print("5. Edit due date")
        print("6. Quit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            toggle_task(tasks)
        elif choice == "5":
            edit_due_date(tasks)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


main()
