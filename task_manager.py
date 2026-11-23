
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, title, priority="Средний"):
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")

        task = {
            "id": self.next_id,
            "title": title.strip(),
            "priority": priority,
            "status": "To Do"
        }

        self.tasks.append(task)
        self.next_id += 1
        return task

    def delete_task(self, task_id):
        self.tasks = [
            task for task in self.tasks
            if task["id"] != task_id
        ]

    def update_status(self, task_id, new_status):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                return True

        return False

    def get_tasks(self, status=None):
        if status is None:
            return self.tasks.copy()

        return [
            task for task in self.tasks
            if task["status"] == status
        ]

    def get_progress(self):
        if not self.tasks:
            return 0

        completed = sum(
            1 for task in self.tasks
            if task["status"] == "Done"
        )

        return round(completed / len(self.tasks) * 100)
