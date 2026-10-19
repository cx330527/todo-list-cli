"""A tiny task manager stored in a JSON file."""

import argparse
import json
from pathlib import Path


def load_tasks(path):
    """Read tasks, returning an empty list when the file does not exist."""
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("无法读取任务文件：{}".format(error)) from error
    if not isinstance(tasks, list) or any(
        not isinstance(task, dict)
        or not isinstance(task.get("id"), int)
        or not isinstance(task.get("title"), str)
        or not isinstance(task.get("done"), bool)
        for task in tasks
    ):
        raise ValueError("任务文件格式不正确。")
    return tasks


def save_tasks(path, tasks):
    """Write tasks as readable JSON."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)
        file.write("\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="简单的待办清单")
    parser.add_argument("--file", type=Path, default=Path("tasks.json"), help="任务文件路径")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="添加任务")
    add.add_argument("title", help="任务内容")
    commands.add_parser("list", help="显示任务")
    done = commands.add_parser("done", help="标记任务已完成")
    done.add_argument("id", type=int, help="任务编号")
    delete = commands.add_parser("delete", help="删除任务")
    delete.add_argument("id", type=int, help="任务编号")
    args = parser.parse_args(argv)

    try:
        tasks = load_tasks(args.file)
    except ValueError as error:
        parser.exit(1, "错误：{}\n".format(error))

    if args.command == "list":
        if not tasks:
            print("还没有任务。")
        for task in tasks:
            mark = "✓" if task["done"] else " "
            print("[{}] {}: {}".format(mark, task["id"], task["title"]))
        return

    if args.command == "add":
        title = args.title.strip()
        if not title:
            parser.error("任务内容不能为空。")
        if any(ord(character) < 32 or ord(character) == 127 for character in title):
            parser.error("任务内容不能包含换行等控制字符。")
        new_id = max((task["id"] for task in tasks), default=0) + 1
        tasks.append({"id": new_id, "title": title, "done": False})
        message = "已添加任务 {}。".format(new_id)
    else:
        task = next((item for item in tasks if item["id"] == args.id), None)
        if task is None:
            parser.error("找不到编号为 {} 的任务。".format(args.id))
        if args.command == "done":
            task["done"] = True
            message = "任务 {} 已完成。".format(args.id)
        else:
            tasks.remove(task)
            message = "已删除任务 {}。".format(args.id)

    try:
        save_tasks(args.file, tasks)
    except OSError as error:
        parser.exit(1, "错误：无法保存任务文件：{}\n".format(error))
    print(message)


if __name__ == "__main__":
    main()
