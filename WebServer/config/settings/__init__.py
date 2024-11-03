# import importlib.util
# import os
# from .settings import *

# CURRENT_DIR = os.getcwd()

# settings_path_user = os.path.join(CURRENT_DIR, "config", "settings.py")
# if os.path.exists(settings_path_user):
#     spec = importlib.util.spec_from_file_location("settings", settings_path_user)
#     settings_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(settings_module)

#     globals().update(vars(settings_module))

import importlib.util
import os
import pathlib
from .settings import *


def load_config():
    # user_config_path = os.path.join(os.getcwd(), "config", "settings.py")
    conf_path = pathlib.Path(os.getcwd()) / "settings" / "settings.py"
    if conf_path.exists():
        spec = importlib.util.spec_from_file_location("settings", conf_path)
        user_conf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_conf)

        # Override defaults with user-provided values
        for key in dir(user_conf):
            if not key.startswith("__"):
                globals()[key] = getattr(user_conf, key)


load_config()
