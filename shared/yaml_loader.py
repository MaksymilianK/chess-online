import yaml


def load(file_name: str, default: dict) -> dict:
    try:
        with open(file_name, "r") as file:
            return yaml.load(file)
    except FileNotFoundError:
        with open(file_name, "w") as file:
            yaml.dump(default, file)
            return default
