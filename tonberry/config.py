import json
import os
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path


@dataclass
class Config:
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    ACCESS_LOGGING: bool = True
    JINJA_TEMPLATE_PATH: str = "."


def config_init() -> Config:
    logger = getLogger("Tonberry")
    env_var_name = "TONBERRY_CONFIG"
    path_str = os.environ.get(env_var_name)
    config_path = Path(path_str or "")
    if not config_path.is_file():
        logger.warning(
            f"Config file path is not valid or not set, loading default values. To use "
            f"a config file set up an environment variable called '{env_var_name}' and "
            f"set the value to a JSON config file path."
        )
        return Config()
    return Config(**json.loads(config_path.open().read()))
