import os
import tkinter as tk
from tkinter import filedialog

import markdown
from tkhtmlview import HTMLScrolledText
from tkinterdnd2 import DND_FILES, TkinterDnD

from settings import Settings
from theme import render_code_blocks, render_lists, wrap_html


try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


settings = Settings(root=None)
current_file = None
last_mtime = 0
watch_job = None


def shorten_path(path: str, max_length: int = 45) -> str:
    if len(path) <= max_length:
        return path
    return "..." + path[-(max_length - 3):]


def update_recent_files(path: str) -> None:
    normalized = os.path.normpath(path)
    recent = [os.path.normpath(item) for item in settings.recent_files if item]
    recent = [item for item in recent if item != normalized]
    recent.insert(0, normalized)
    settings.recent_files = recent[:5]
    settings.last_file = normalized
    settings.save()
    refresh_recent_menu()


def open_path(path: str) -> None:
    global current_file, last_mtime

    if not path or not os.path.exists(path):
        return

    current_file = path
    last_mtime = 0
    update_recent_files(path)
    load_md()
    schedule_load_watch()


root = TkinterDnD.Tk()
root.title("Markdown Viewer")
root.geometry("900x650")
root.configure(bg="#f3f3f3")
root.attributes("-alpha", settings.alpha)
root.attributes("-topmost", settings.topmost)
settings.bind_root(root)


toolbar = tk.Frame(root, bg="#f3f3f3", bd=1, relief="solid")
toolbar.pack(fill="x")


file_btn = tk.Menubutton(
    toolbar,
    text="File",
    relief="flat",
    bg="#f3f3f3",
    activebackground="#e8e8e8",
    bd=0,
    padx=10,
    pady=6,
)
file_btn.pack(side="left", padx=8, pady=4)

file_menu = tk.Menu(file_btn, tearoff=0)
file_btn.config(menu=file_menu)


def render(md_text: str) -> None:
    html = markdown.markdown(
        md_text,
        extensions=["extra", "tables", "fenced_code", "nl2br"],
    )
    html = render_code_blocks(html)
    html = render_lists(html)
    viewer.set_html(wrap_html(html, settings))
    apply_selection_style()


def apply_selection_style() -> None:
    viewer.config(
        selectbackground="#000000",
        selectforeground="#ffffff",
        inactiveselectbackground="#000000",
    )
    viewer.tag_configure("sel", background="#000000", foreground="#ffffff")
    viewer.tag_raise("sel")


def has_selection() -> bool:
    try:
        return bool(viewer.tag_ranges("sel"))
    except tk.TclError:
        return False


def copy_selection(event=None):
    if not has_selection():
        return "break"

    try:
        selected_text = viewer.get("sel.first", "sel.last")
    except tk.TclError:
        return "break"

    root.clipboard_clear()
    root.clipboard_append(selected_text)
    return "break"


def select_all(event=None):
    viewer.focus_set()
    viewer.tag_remove("sel", "1.0", "end")
    viewer.tag_add("sel", "1.0", "end-1c")
    viewer.mark_set("insert", "1.0")
    viewer.yview_moveto(0.0)
    return "break"


def clear_selection(event=None):
    viewer.tag_remove("sel", "1.0", "end")
    return "break"


def select_word(event):
    viewer.focus_set()
    index = viewer.index(f"@{event.x},{event.y}")
    viewer.tag_remove("sel", "1.0", "end")
    viewer.tag_add("sel", f"{index} wordstart", f"{index} wordend")
    viewer.mark_set("insert", f"{index} wordend")
    return "break"


def select_line(event):
    viewer.focus_set()
    index = viewer.index(f"@{event.x},{event.y}")
    viewer.tag_remove("sel", "1.0", "end")
    viewer.tag_add("sel", f"{index} linestart", f"{index} lineend")
    viewer.mark_set("insert", f"{index} lineend")
    viewer.see("insert")
    return "break"


def show_viewer_menu(event) -> str:
    viewer.focus_set()
    copy_menu.entryconfig("Copy", state=("normal" if has_selection() else "disabled"))
    copy_menu.entryconfig("Select All", state="normal")
    copy_menu.tk_popup(event.x_root, event.y_root)
    copy_menu.grab_release()
    return "break"


def refresh() -> None:
    settings.save()

    if font_var.get() != str(settings.font_size):
        font_var.set(str(settings.font_size))
    if line_var.get() != str(settings.line_height):
        line_var.set(str(settings.line_height))
    if alpha_var.get() != str(settings.alpha):
        alpha_var.set(str(settings.alpha))

    if current_file and os.path.exists(current_file):
        with open(current_file, "r", encoding="utf-8") as f:
            render(f.read())


def load_md() -> None:
    global last_mtime

    if current_file and os.path.exists(current_file):
        mtime = os.path.getmtime(current_file)
        if mtime != last_mtime:
            last_mtime = mtime
            with open(current_file, "r", encoding="utf-8") as f:
                render(f.read())


def schedule_load_watch() -> None:
    global watch_job

    if watch_job is not None:
        root.after_cancel(watch_job)
    watch_job = root.after(1000, watch_and_reload)


def watch_and_reload() -> None:
    global watch_job

    watch_job = None
    load_md()
    schedule_load_watch()


def open_file() -> None:
    path = filedialog.askopenfilename(filetypes=[("Markdown Files", "*.md")])
    if path:
        open_path(path)


def open_recent_file(path: str) -> None:
    if os.path.exists(path):
        open_path(path)
        return

    recent = [item for item in settings.recent_files if os.path.exists(item)]
    settings.recent_files = recent
    if settings.last_file == path:
        settings.last_file = recent[0] if recent else ""
    settings.save()
    refresh_recent_menu()


def refresh_recent_menu() -> None:
    recent_menu.delete(0, "end")

    valid_recent = [item for item in settings.recent_files if item]
    if not valid_recent:
        recent_menu.add_command(label="No Recent Files", state="disabled")
        return

    for path in valid_recent[:5]:
        recent_menu.add_command(
            label=shorten_path(path),
            command=lambda p=path: open_recent_file(p),
        )


def toggle_settings_panel() -> None:
    global settings_popup

    if settings_popup and settings_popup.winfo_exists():
        settings_popup.lift()
        settings_popup.focus_force()
        return

    settings_popup = tk.Toplevel(root)
    settings_popup.title("Settings")
    settings_popup.transient(root)
    settings_popup.resizable(False, False)
    settings_popup.configure(bg="#f3f3f3")
    settings_popup.withdraw()

    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    popup_x = root_x + 60
    popup_y = root_y + 70
    settings_popup.geometry(f"+{popup_x}+{popup_y}")

    panel = tk.Frame(
        settings_popup,
        bg="#f3f3f3",
        bd=1,
        relief="solid",
        padx=14,
        pady=14,
    )
    panel.pack(fill="both", expand=True, padx=10, pady=10)

    title_row = tk.Frame(panel, bg="#f3f3f3")
    title_row.pack(fill="x", pady=(0, 10))
    tk.Label(
        title_row,
        text="Viewer Settings",
        bg="#f3f3f3",
        fg="#1f1f1f",
        font=("Segoe UI", 10, "bold"),
    ).pack(side="left")

    close_btn = tk.Button(
        title_row,
        text="Close",
        command=settings_popup.destroy,
        bg="#f3f3f3",
        activebackground="#e8e8e8",
        relief="flat",
        bd=0,
        padx=8,
        pady=2,
        font=("Segoe UI", 9),
    )
    close_btn.pack(side="right")

    font_row = tk.Frame(panel, bg="#f3f3f3")
    font_row.pack(fill="x", pady=4)
    tk.Label(
        font_row,
        text="Font Size",
        bg="#f3f3f3",
        width=12,
        anchor="w",
        font=("Segoe UI", 9),
    ).pack(side="left")
    tk.Entry(
        font_row,
        textvariable=font_var,
        width=8,
        relief="solid",
        bd=1,
        font=("Segoe UI", 9),
    ).pack(side="left")
    tk.Label(font_row, text="px", bg="#f3f3f3", font=("Segoe UI", 9)).pack(side="left", padx=(8, 0))

    line_row = tk.Frame(panel, bg="#f3f3f3")
    line_row.pack(fill="x", pady=4)
    tk.Label(
        line_row,
        text="Line Height",
        bg="#f3f3f3",
        width=12,
        anchor="w",
        font=("Segoe UI", 9),
    ).pack(side="left")
    tk.Entry(
        line_row,
        textvariable=line_var,
        width=8,
        relief="solid",
        bd=1,
        font=("Segoe UI", 9),
    ).pack(side="left")

    alpha_row = tk.Frame(panel, bg="#f3f3f3")
    alpha_row.pack(fill="x", pady=4)
    tk.Label(
        alpha_row,
        text="Opacity",
        bg="#f3f3f3",
        width=12,
        anchor="w",
        font=("Segoe UI", 9),
    ).pack(side="left")
    tk.Entry(
        alpha_row,
        textvariable=alpha_var,
        width=8,
        relief="solid",
        bd=1,
        font=("Segoe UI", 9),
    ).pack(side="left")

    top_row = tk.Frame(panel, bg="#f3f3f3")
    top_row.pack(fill="x", pady=(10, 4))
    tk.Checkbutton(
        top_row,
        text="Always On Top",
        variable=is_topmost,
        command=toggle_topmost,
        bg="#f3f3f3",
        activebackground="#f3f3f3",
        font=("Segoe UI", 9),
    ).pack(side="left")

    settings_popup.protocol("WM_DELETE_WINDOW", settings_popup.destroy)
    settings_popup.update_idletasks()
    settings_popup.deiconify()
    settings_popup.focus_force()


def on_font(*_) -> None:
    try:
        settings.font_size = int(font_var.get())
        refresh()
    except ValueError:
        pass


def on_line(*_) -> None:
    try:
        settings.line_height = float(line_var.get())
        refresh()
    except ValueError:
        pass


def on_alpha(*_) -> None:
    try:
        value = float(alpha_var.get())
        settings.alpha = value
        root.attributes("-alpha", value)
        settings.save()
    except ValueError:
        pass


def toggle_topmost() -> None:
    settings.topmost = is_topmost.get()


def drop_file(event) -> None:
    path = event.data.strip("{}")
    if path.lower().endswith(".md"):
        open_path(path)


file_menu.add_command(label="Open File", command=open_file)
recent_menu = tk.Menu(file_menu, tearoff=0)
file_menu.add_cascade(label="Recent Files", menu=recent_menu)


settings_btn = tk.Menubutton(toolbar, text="Settings", relief="flat")
settings_btn.configure(
    bg="#f3f3f3",
    activebackground="#e8e8e8",
    bd=0,
    padx=10,
    pady=6,
)
settings_btn.pack(side="left", padx=8, pady=4)
settings_btn.bind("<Button-1>", lambda e: toggle_settings_panel())

font_var = tk.StringVar(value=str(settings.font_size))
font_var.trace_add("write", on_font)

line_var = tk.StringVar(value=str(settings.line_height))
line_var.trace_add("write", on_line)

alpha_var = tk.StringVar(value=str(settings.alpha))
alpha_var.trace_add("write", on_alpha)


is_topmost = tk.BooleanVar(value=settings.topmost)
settings_popup = None


viewer = HTMLScrolledText(
    root,
    html="<h2>Markdown Viewer</h2>",
    background="#ffffff",
    padx=28,
    pady=24,
)
viewer.config(
    bd=1,
    relief="solid",
    highlightthickness=0,
    cursor="xterm",
    wrap="word",
    selectbackground="#000000",
    selectforeground="#ffffff",
    inactiveselectbackground="#000000",
)
apply_selection_style()
viewer.pack(fill="both", expand=True)

copy_menu = tk.Menu(root, tearoff=0)
copy_menu.add_command(label="Copy", command=copy_selection)
copy_menu.add_command(label="Select All", command=select_all)

viewer.bind("<Control-c>", copy_selection)
viewer.bind("<Control-C>", copy_selection)
viewer.bind("<Control-a>", select_all)
viewer.bind("<Control-A>", select_all)
viewer.bind("<Escape>", clear_selection)
viewer.bind("<Double-Button-1>", select_word)
viewer.bind("<Triple-Button-1>", select_line)
viewer.bind("<<Selection>>", lambda e: apply_selection_style())
viewer.bind("<Button-3>", show_viewer_menu)


root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", drop_file)


refresh_recent_menu()
if settings.last_file and os.path.exists(settings.last_file):
    open_path(settings.last_file)

schedule_load_watch()
root.mainloop()
