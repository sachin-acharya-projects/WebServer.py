import importlib.util
import os
from .Settings import *

CURRENT_DIR = os.getcwd()

settings_path_user = os.path.join(CURRENT_DIR, "Configurations", "Settings.py")
if os.path.exists(settings_path_user):
    spec = importlib.util.spec_from_file_location("Settings", settings_path_user)
    settings_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings_module)

    globals().update(vars(settings_module))
