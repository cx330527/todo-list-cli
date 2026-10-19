import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

from main import load_tasks, main


class TodoTests(unittest.TestCase):
    def test_add_complete_delete_and_persist(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"
            options = ["--file", str(path)]
            main(options + ["add", "学习 Python"])
            main(options + ["add", "练习算法"])
            main(options + ["done", "1"])
            self.assertEqual(load_tasks(path), [
                {"id": 1, "title": "学习 Python", "done": True},
                {"id": 2, "title": "练习算法", "done": False},
            ])
            main(options + ["delete", "1"])
            self.assertEqual([task["id"] for task in load_tasks(path)], [2])

    def test_bad_json_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"
            path.write_text("broken", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tasks(path)

    def test_control_characters_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                main(["--file", str(path), "add", "safe\x1b[31m"])
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
