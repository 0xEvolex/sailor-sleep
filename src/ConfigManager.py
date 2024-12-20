import os
import json

class ConfigManager:
    config_file = "config.txt"
    default_config = {
        "AudioFilePath": "C:/Users/example_user/example_sound.mp3",
        "scanForDisconnect": True,
        "scanForDeath": True,
        "scanForIngame": True,
        "deathDelay": 120
    }

    @staticmethod
    def save(config):
        with open(ConfigManager.config_file, "w") as file:
            json.dump(config, file)
        print(f"[INFO] Config saved: '{os.getcwd()}\\{ConfigManager.config_file}'")

    @staticmethod
    def load():
        if not os.path.exists(ConfigManager.config_file) or os.path.getsize(ConfigManager.config_file) == 0:
            ConfigManager._create()
            print(f"[INFO] Config created: '{os.getcwd()}\\{ConfigManager.config_file}'")
        with open(ConfigManager.config_file, "r") as file:
            config = json.load(file)
        print(f"[INFO] Config loaded: '{os.getcwd()}\\{ConfigManager.config_file}'")
        return config

    @staticmethod
    def _create():
        with open(ConfigManager.config_file, "w") as file:
            json.dump(ConfigManager.default_config, file)