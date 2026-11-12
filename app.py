"""
Entrypoint raíz para Streamlit Cloud.
Redirige directamente al aplicativo principal en 06_App/app.py.
"""
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_APP_DIR = _ROOT / "06_App"
_SRC_DIR = _APP_DIR / "src"
_UI_DIR = _APP_DIR / "ui"

for p in [str(_SRC_DIR), str(_UI_DIR), str(_APP_DIR), str(_ROOT)]:
    while p in sys.path:
        sys.path.remove(p)
    sys.path.insert(0, p)

if "src" in sys.modules:
    try:
        mod = sys.modules["src"]
        if not hasattr(mod, "__file__") or "06_App" not in getattr(mod, "__file__", ""):
            del sys.modules["src"]
    except Exception:
        pass

try:
    from app import main
except (ImportError, ModuleNotFoundError):
    import importlib.util
    spec = importlib.util.spec_from_file_location("kibo_app", str(_APP_DIR / "app.py"))
    kibo_app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kibo_app)
    main = kibo_app.main

if __name__ == "__main__":
    main()
