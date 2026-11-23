
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from task_manager import TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        task = self.manager.add_task("Изучить Python")
        self.assertEqual(task["title"], "Изучить Python")
        self.assertEqual(task["status"], "To Do")

    def test_delete_task(self):
        task = self.manager.add_task("Тестовая задача")
        self.manager.delete_task(task["id"])
        self.assertEqual(len(self.manager.get_tasks()), 0)

    def test_update_status(self):
        task = self.manager.add_task("Тестовая задача")
        self.manager.update_status(task["id"], "Done")
        self.assertEqual(task["status"], "Done")

    def test_progress(self):
        self.manager.add_task("Задача 1")
        task = self.manager.add_task("Задача 2")
        self.manager.update_status(task["id"], "Done")
        self.assertEqual(self.manager.get_progress(), 50)


if __name__ == "__main__":
    unittest.main()
