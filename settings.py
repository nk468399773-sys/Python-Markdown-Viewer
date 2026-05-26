import json
import os


CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "bg_color": "#ffffff",
    "font_size": 14,
    "line_height": 1.7,
    "alpha": 1.0,
    "topmost": True,
    "last_file": "",
    "recent_files": [],
}


class Settings:
    def __init__(self, root=None):
        self.root = root
        self.data = self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def save(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def _ensure_defaults(self):
        changed = False
        for key, value in DEFAULT_CONFIG.items():
            if key not in self.data:
                if isinstance(value, list):
                    self.data[key] = value.copy()
                else:
                    self.data[key] = value
                changed = True
        if changed:
            self.save()

    def bind_root(self, root):
        self.root = root
        self._ensure_defaults()
        self.apply_topmost()

    def apply_topmost(self):
        if self.root:
            self.root.attributes("-topmost", self.data["topmost"])
        self.save()

    @property
    def bg_color(self):
        return self.data["bg_color"]

    @bg_color.setter
    def bg_color(self, value):
        self.data["bg_color"] = value

    @property
    def font_size(self):
        return self.data["font_size"]

    @font_size.setter
    def font_size(self, value):
        self.data["font_size"] = value

    @property
    def line_height(self):
        return self.data["line_height"]

    @line_height.setter
    def line_height(self, value):
        self.data["line_height"] = value

    @property
    def alpha(self):
        return self.data["alpha"]

    @alpha.setter
    def alpha(self, value):
        self.data["alpha"] = value

    @property
    def topmost(self):
        return self.data["topmost"]

    @topmost.setter
    def topmost(self, value):
        self.data["topmost"] = value
        self.apply_topmost()

    @property
    def last_file(self):
        return self.data["last_file"]

    @last_file.setter
    def last_file(self, value):
        self.data["last_file"] = value

    @property
    def recent_files(self):
        return self.data["recent_files"]

    @recent_files.setter
    def recent_files(self, value):
        self.data["recent_files"] = value
