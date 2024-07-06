# Autosink 项目的数据提取-加载-转换

[🇬🇧](README.md) | [🇰🇷](README.kr.md) | [🇨🇳](README.zh-CN.md)

将数据湖中的值解析并加载到内存中，然后使数据标记器可以运行。autosink-data-elt 包含了用于很好地读取和写入数据湖中存储的 json 文件的实用类，以及定义了数据类型。当从树莓派提取的数据存储在数据湖中时，将数据加载并标记，然后将转换后的数据存储到特征存储中，因此将其命名为 ELT。

## 功能

- [ ] 解析数据湖中的值并将其加载到内存中，然后整理为数据标记器方便读取的形式。
- [ ] 调用标记器。
- [ ] 将标记完成的数据存储到特征存储中。

# 环境

环境基于 MacOS 和 Linux。

## `Makefile`

`Makefile` 具有以下功能。

### `make lint`

- 要使用 `.vscode` 设置，请安装 `pylint` 扩展。
- 使用默认的 linter 设置，覆盖在 `pyproject.toml` 文件中指定的选项来进行代码检查。

### `make format`

- 格式化程序使用 google 的 `yapf`。
- 使用 `pyproject.toml` 文件中指定的选项来覆盖 `yapf` 格式化程序的默认设置来格式化代码。
- 要使用 `.vscode` 设置，请安装 `yapf` 扩展。

### `make test`

- 使用 `unittest` 进行测试。
- 支持 `test_*.py` 和 `*_test.py` 模式。
- 测试文件必须连接到包含测试文件的位置，且连接到 `__init__.py`。

### `make publish`

- 请在 `~/.