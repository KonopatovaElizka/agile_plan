
import tkinter as tk
from tkinter import ttk, messagebox

from task_manager import TaskManager
from storage import save_tasks, load_tasks


class AgilePlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Agile Planner")
        self.root.geometry("750x550")
        self.root.minsize(650, 450)

        self.manager = TaskManager()
        self.manager.tasks = load_tasks()

        if self.manager.tasks:
            self.manager.next_id = max(
                task["id"] for task in self.manager.tasks
            ) + 1

        self.create_interface()
        self.refresh_tasks()

    def create_interface(self):
        title = ttk.Label(
            self.root,
            text="Agile Planner",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill="x", padx=20, pady=10)

        self.task_entry = ttk.Entry(input_frame)
        self.task_entry.pack(
            side="left", fill="x", expand=True, padx=(0, 10)
        )

        self.priority_box = ttk.Combobox(
            input_frame,
            values=["Низкий", "Средний", "Высокий"],
            state="readonly",
            width=12
        )
        self.priority_box.set("Средний")
        self.priority_box.pack(side="left", padx=5)

        ttk.Button(
            input_frame,
            text="Добавить",
            command=self.add_task
        ).pack(side="left", padx=5)

        columns = ("id", "title", "priority", "status")

        self.task_table = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=12
        )

        self.task_table.heading("id", text="ID")
        self.task_table.heading("title", text="Задача")
        self.task_table.heading("priority", text="Приоритет")
        self.task_table.heading("status", text="Статус")

        self.task_table.column("id", width=45, anchor="center")
        self.task_table.column("title", width=300)
        self.task_table.column("priority", width=100, anchor="center")
        self.task_table.column("status", width=120, anchor="center")

        self.task_table.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=10)

        ttk.Button(
            buttons_frame,
            text="Удалить задачу",
            command=self.delete_task
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="Изменить статус",
            command=self.change_status
        ).pack(side="left", padx=5)

        self.progress_label = ttk.Label(
            self.root,
            text="Прогресс: 0%"
        )
        self.progress_label.pack(pady=10)

    def refresh_tasks(self):
        for item in self.task_table.get_children():
            self.task_table.delete(item)

        for task in self.manager.get_tasks():
            self.task_table.insert(
                "",
                "end",
                values=(
                    task["id"],
                    task["title"],
                    task["priority"],
                    task["status"]
                )
            )

        progress = self.manager.get_progress()
        self.progress_label.config(
            text=f"Прогресс выполнения: {progress}%"
        )

        save_tasks(self.manager.tasks)

    def add_task(self):
        title = self.task_entry.get()

        try:
            self.manager.add_task(
                title,
                self.priority_box.get()
            )
        except ValueError as error:
            messagebox.showwarning("Ошибка", str(error))
            return

        self.task_entry.delete(0, tk.END)
        self.refresh_tasks()

    def delete_task(self):
        selected = self.task_table.selection()

        if not selected:
            messagebox.showwarning(
                "Внимание", "Выберите задачу для удаления"
            )
            return

        task_id = int(
            self.task_table.item(selected[0], "values")[0]
        )

        self.manager.delete_task(task_id)
        self.refresh_tasks()

    def change_status(self):
        selected = self.task_table.selection()

        if not selected:
            messagebox.showwarning(
                "Внимание", "Выберите задачу"
            )
            return

        task_id = int(
            self.task_table.item(selected[0], "values")[0]
        )

        statuses = ["To Do", "In Progress", "Done"]

        status_window = tk.Toplevel(self.root)
        status_window.title("Изменение статуса")
        status_window.geometry("250x130")
        status_window.resizable(False, False)

        status_box = ttk.Combobox(
            status_window,
            values=statuses,
            state="readonly"
        )
        status_box.set(statuses[0])
        status_box.pack(pady=15)

        def save_status():
            self.manager.update_status(
                task_id,
                status_box.get()
            )
            self.refresh_tasks()
            status_window.destroy()

        ttk.Button(
            status_window,
            text="Сохранить",
            command=save_status
        ).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = AgilePlanner(root)
    root.mainloop()
