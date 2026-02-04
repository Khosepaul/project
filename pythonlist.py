FILE_NAME = "tasks.txt"


def load_tasks():
    try:
        with open(FILE_NAME, "r") as file:  
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(task + "\n")


def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
    else:
        print("\nYour Tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")


def add_task(tasks):
    task = input("Enter a new task: ").strip()
    if task:
        tasks.append(task)
        save_tasks(tasks)
        print("Task added.")
    else:
        print("Task cannot be empty.")


def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return


    try:
        num = int(input("Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks(tasks)
            print(f"Deleted task: {removed}")
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
        print("4. Quit")


        choice = input("Choose an option (1-4): ")


        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


main()