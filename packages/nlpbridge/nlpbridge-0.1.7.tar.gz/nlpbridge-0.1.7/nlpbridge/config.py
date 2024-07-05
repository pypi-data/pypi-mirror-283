import yaml
import os
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# relative_path = "config.yaml"
# yaml_path = os.path.join(project_root, relative_path)

yaml_path = os.getenv("CONFIG_PATH")
CONFIG = None


def reload_config(yaml_path):
    global CONFIG

    with open(yaml_path, 'r') as file:
        CONFIG = yaml.safe_load(file)

        if CONFIG is None:
            raise Exception("Config file is empty")


reload_config(yaml_path)
