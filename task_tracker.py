import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import threading

# Define a class to represent a Task
class Task:
    def __init__(self, title, description, duration):
        self.title = title
        self.description = description
        self.duration = duration
        self.completed = False

# Define the main application class
class TaskTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker")

        self.tasks = []  # List to store Task objects

        # Create GUI elements
        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=10, width=50)
        self.task_listbox.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Task", command=self.start_task)
        self.start_button.pack()

        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.exit_button = tk.Button(root, text="Exit", command=root.destroy)
        self.exit_button.pack()

        # Sample tasks for testing
        task1 = Task("Task 1", "Description for Task 1", 1)  # Reduced duration for testing
        task2 = Task("Task 2", "Description for Task 2", 1)
        self.tasks.append(task1)
        self.tasks.append(task2)
        self.update_task_listbox()

    # Function to start a selected task with a countdown
    def start_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            messagebox.showinfo("Task Started", f"Timer started for task: {selected_task.title}")

            # Function to run the countdown in a separate thread
            def countdown():
                for remaining in range(selected_task.duration * 60, -1, -1):
                    mins, secs = divmod(remaining, 60)
                    timeformat = "{:02d}:{:02d}".format(mins, secs)
                    self.root.title(f"Task Tracker - {timeformat}")
                    time.sleep(1)

                selected_task.completed = True
                messagebox.showinfo("Task Completed", f"Task completed: {selected_task.title}")
                self.root.title("Task Tracker")
                self.update_task_listbox()

            # Run countdown in a separate thread to not block the GUI
            threading.Thread(target=countdown).start()

    # Function to add a new task
    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task title:")
        description = simpledialog.askstring("Add Task", "Enter task description:")
        duration = simpledialog.askinteger("Add Task", "Enter task duration (in minutes):")
        new_task = Task(title, description, duration)
        self.tasks.append(new_task)
        self.update_task_listbox()

    # Function to delete a selected task
    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.update_task_listbox()

    # Function to update the task listbox
    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Completed" if task.completed else "Not Completed"
            self.task_listbox.insert(tk.END, f"{task.title} - {status}")

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()