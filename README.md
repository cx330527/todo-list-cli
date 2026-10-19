# 命令行待办清单

用 Python 管理待办事项的入门项目。可以添加、查看、完成和删除任务，任务保存在本机 JSON 文件中。

## 运行

需要 Python 3.9 或更新版本，无需安装第三方库。在项目目录运行：

```text
python main.py add "学习 Python"
python main.py add "练习算法"
python main.py list
python main.py done 1
python main.py delete 2
```

默认保存到当前目录的 `tasks.json`。所有 `.json` 文件都已被 `.gitignore` 排除，不会随正常 Git 提交上传。可以用 `--file` 选择其他位置：

```text
python main.py --file my-tasks.json list
```

任务编号用于 `done` 和 `delete` 命令。删除任务不会改变其他任务的编号。

## 学习要点

- `argparse` 解析子命令。
- `json` 在本地保存数据。
- 列表和字典存储任务。
- 检查输入和损坏的 JSON 文件。

## 测试

```text
python -m unittest discover -s tests -v
```

程序没有网络功能。任务内容只写入你指定的本地文件，请不要把自己的 `tasks.json` 手动上传到公开仓库。许可证见 [LICENSE](LICENSE)。
