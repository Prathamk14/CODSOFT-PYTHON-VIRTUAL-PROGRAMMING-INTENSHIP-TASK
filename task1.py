from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

class TaskManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")
        self.master.geometry("750x400")
        self.master.resizable(0, 0)
        self.master.configure(bg="#E0E0E0")

        # Database connection
        self.connection = sql.connect('ListOfTasks.db')
        self.the_cursor = self.connection.cursor()
        self.the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks(title TEXT)')

        # Task list
        self.tasks = []

        # Function frame
        self.function_frame = Frame(self.master, bg="#E0E0E0")
        self.function_frame.pack(side="top", expand=True, fill="both")

        # Labels and Entry
        Label(self.function_frame, text="Enter Task:", font=("Arial", 14, "bold"), bg="#E0E0E0", fg="#004080").grid(row=0, column=0, padx=10, pady=10)
        self.task_entry = Entry(self.function_frame, font=("Arial", 14), width=42, fg="#004080", bg="white")
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)

        # Buttons
        Button(self.function_frame, text="Add Task", width=11, height=2, bg="#FFD699", font=("Arial", 14, "bold"), command=self.add_task).grid(row=1, column=0, pady=10)
        Button(self.function_frame, text="Delete Task", width=11, height=2, bg="#FFD699", font=("Arial", 14, "bold"), command=self.delete_task).grid(row=1, column=1, pady=10)
        Button(self.function_frame, text="Delete All", width=11, height=2, bg="#FFD699", font=("Arial", 14, "bold"), command=self.delete_all_tasks).grid(row=1, column=2, pady=10)
        Button(self.function_frame, text="Exit", width=52, height=2, bg="#FFD699", font=("Arial", 14, "bold"), command=self.close_app).grid(row=3, column=0, columnspan=3, pady=10)

        # Task Listbox
        self.task_listbox = Listbox(self.function_frame, width=57, height=7, font=("Arial", 12), selectmode='SINGLE', bg='white', fg='#004080', selectbackground="#FFD699", selectforeground="#004080")
        self.task_listbox.grid(row=2, column=0, columnspan=3, pady=10)

        # Initialize tasks
        self.retrieve_tasks()
        self.update_tasks()

    def add_task(self):
        task_text = self.task_entry.get()
        if len(task_text) == 0:
            messagebox.showinfo('Error', 'Task field is empty')
        else:
            self.tasks.append(task_text)
            self.the_cursor.execute('INSERT INTO tasks VALUES (?)', (task_text,))
            self.update_tasks()
            self.task_entry.delete(0, 'end')

    def update_tasks(self):
        self.clear_tasks()
        for task in self.tasks:
            self.task_listbox.insert('end', task)

    def delete_task(self):
        try:
            selected_task = self.task_listbox.get(self.task_listbox.curselection())
            if selected_task in self.tasks:
                self.tasks.remove(selected_task)
                self.update_tasks()
                self.the_cursor.execute('DELETE FROM tasks WHERE title = ?', (selected_task,))
        except TclError:
            messagebox.showinfo('Error', 'No task selected.')

    def delete_all_tasks(self):
        confirm_delete = messagebox.askyesno('Delete All', 'Are you sure you want to delete all tasks?')
        if confirm_delete:
            self.tasks.clear()
            self.the_cursor.execute('DELETE FROM tasks')
            self.update_tasks()
            messagebox.showinfo('Delete All', 'All tasks deleted')

    def clear_tasks(self):
        self.task_listbox.delete(0, 'end')

    def close_app(self):
        self.connection.commit()
        self.the_cursor.close()
        self.master.destroy()

    def retrieve_tasks(self):
        self.tasks.clear()
        for row in self.the_cursor.execute('SELECT title FROM tasks'):
            self.tasks.append(row[0])

if __name__ == "__main__":
    root = Tk()
    app = TaskManager(root)
    root.mainloop()
