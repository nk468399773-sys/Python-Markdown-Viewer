# Markdown Viewer

一个面向 Windows 使用场景的轻量级 Markdown 预览器，基于 `tkinter`、`tkinterdnd2` 和 `tkhtmlview` 构建。

它支持 Markdown 文件实时预览、拖拽打开、最近文件记录、弹出式设置面板，以及基础的文字选中与复制功能。

## 功能特性

- 通过 `File` 菜单打开本地 `.md` 文件
- 支持将 Markdown 文件拖拽到窗口中直接打开
- 当前文件内容变更后自动刷新
- 启动时自动恢复上一次打开的文件
- 最多保存 5 条最近打开记录
- 提供弹出式设置窗口，可调整：
  - 字体大小
  - 行距
  - 窗口透明度
  - 窗口置顶
- 支持的 Markdown 内容包括：
  - 标题
  - 段落
  - 手动换行
  - 表格
  - 围栏代码块
  - 简单无序列表
- 支持基础文字交互：
  - 选中文字
  - `Ctrl+C` 复制
  - `Ctrl+A` 全选
  - `Esc` 取消选中
  - 双击选词
  - 三击选中当前整行
  - 右键上下文菜单

## 运行环境

- Windows
- Python 3.11，或兼容的 Python 3 版本

## 安装依赖

在项目目录中执行：

```powershell
pip install -r requirements.txt
```

如果你希望使用指定 Python 路径：

```powershell
& 'C:\Users\ASUS\AppData\Local\Programs\Python\Python311\python.exe' -m pip install -r requirements.txt
```

## 启动项目

```powershell
python main.py
```

或者显式指定解释器：

```powershell
& 'C:\Users\ASUS\AppData\Local\Programs\Python\Python311\python.exe' main.py
```

## 使用说明

### 打开文件

- 点击 `File -> Open File`
- 或者直接把 `.md` 文件拖到窗口中

### 最近文件

- 点击 `File -> Recent Files`
- 程序最多记录 5 条最近打开路径
- 如果上一次打开的文件仍然存在，程序启动时会自动恢复

### 设置面板

点击 `Settings` 打开弹出式设置窗口，可调整：

- `Font Size`
- `Line Height`
- `Opacity`
- `Always On Top`

这些设置会在运行时自动保存到 [config.json](D:\桌面\homework\Project\Markdown\config.json)。

## 快捷键与鼠标操作

- `Ctrl+C`：复制当前选中文本
- `Ctrl+A`：全选全文
- `Esc`：取消当前选中
- 双击左键：选中当前单词
- 三击左键：选中当前整行
- 右键：打开上下文菜单

## 项目结构

- [main.py](D:\桌面\homework\Project\Markdown\main.py)：主窗口、文件打开、自动刷新、最近文件、选中复制等逻辑
- [settings.py](D:\桌面\homework\Project\Markdown\settings.py)：配置读写、最近文件和上次文件记录
- [theme.py](D:\桌面\homework\Project\Markdown\theme.py)：代码块、列表和内容包装的 HTML 后处理
- [config.json](D:\桌面\homework\Project\Markdown\config.json)：运行时保存的配置文件
- [requirements.txt](D:\桌面\homework\Project\Markdown\requirements.txt)：依赖列表

## 说明

- 本项目基于 `tkhtmlview` 渲染内容，因此部分复杂 HTML/CSS 行为做了简化处理。
- 为了让代码块和无序列表显示更稳定，项目在 Python 层做了一部分 HTML 后处理。
- 最近文件路径会以普通字符串形式保存在 `config.json` 中。
