import importlib.util
import os
import pathlib
from .settings import *  # noqa: F403


def load_config():
    conf_path = pathlib.Path(os.getcwd()) / "config" / "settings.py"
    module_name = "settings"
    if conf_path.exists():
        spec = importlib.util.spec_from_file_location(module_name, conf_path)
        if spec:
            user_conf = importlib.util.module_from_spec(spec)
            if spec.loader:
                spec.loader.exec_module(user_conf)

            for key in dir(user_conf):
                if not key.startswith("__"):
                    globals()[key] = getattr(user_conf, key)


load_config()