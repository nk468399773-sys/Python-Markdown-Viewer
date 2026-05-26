# Markdown Viewer

A lightweight Windows-oriented Markdown viewer built with `tkinter`, `tkinterdnd2`, and `tkhtmlview`.

It supports live preview, drag-and-drop opening, recent files, a popup settings panel, and basic text selection/copy interactions.

## Features

- Open local `.md` files from the `File` menu
- Drag and drop Markdown files into the window
- Auto-reload when the current file changes on disk
- Restore the last opened file on next launch
- Keep up to 5 recent file paths
- Popup settings window for:
  - font size
  - line height
  - window opacity
  - always-on-top
- Markdown support for:
  - headings
  - paragraphs
  - line breaks
  - tables
  - fenced code blocks
  - simple unordered lists
- Text interaction support:
  - select text
  - `Ctrl+C` copy
  - `Ctrl+A` select all
  - `Esc` clear selection
  - double-click to select a word
  - triple-click to select a line
  - right-click context menu

## Requirements

- Windows
- Python 3.11 or compatible Python 3 version

## Install

Install dependencies in the project directory:

```powershell
pip install -r requirements.txt
```

If you want to use a specific Python executable:

```powershell
& 'C:\Users\ASUS\AppData\Local\Programs\Python\Python311\python.exe' -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

Or with the explicit Python path:

```powershell
& 'C:\Users\ASUS\AppData\Local\Programs\Python\Python311\python.exe' main.py
```

## Usage

### Open a file

- Click `File -> Open File`
- Or drag a `.md` file into the viewer window

### Recent files

- Click `File -> Recent Files`
- The app stores up to 5 recent paths
- The last opened file is restored automatically at startup if it still exists

### Settings

Click `Settings` to open the popup panel and adjust:

- `Font Size`
- `Line Height`
- `Opacity`
- `Always On Top`

Settings are saved to [config.json](D:\桌面\homework\Project\Markdown\config.json) at runtime.

## Keyboard And Mouse Shortcuts

- `Ctrl+C`: Copy selected text
- `Ctrl+A`: Select all text
- `Esc`: Clear selection
- Double-click: Select word
- Triple-click: Select current line
- Right-click: Open context menu

## Project Structure

- [main.py](D:\桌面\homework\Project\Markdown\main.py): main window, file watching, menus, selection and copy behavior
- [settings.py](D:\桌面\homework\Project\Markdown\settings.py): persistent app settings and recent file storage
- [theme.py](D:\桌面\homework\Project\Markdown\theme.py): HTML post-processing for code blocks, lists, and wrapped content
- [config.json](D:\桌面\homework\Project\Markdown\config.json): saved runtime configuration
- [requirements.txt](D:\桌面\homework\Project\Markdown\requirements.txt): Python dependencies

## Notes

- This project uses `tkhtmlview`, so some HTML/CSS behavior is intentionally simplified.
- Code blocks and unordered lists are post-processed in Python to improve rendering consistency.
- Recent file paths are stored as plain strings in `config.json`.
