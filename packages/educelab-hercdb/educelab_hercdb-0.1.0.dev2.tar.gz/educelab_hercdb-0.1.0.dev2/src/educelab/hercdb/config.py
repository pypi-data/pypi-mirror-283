import json
import os
from functools import lru_cache
from pathlib import Path

from prompt_toolkit import prompt
from getpass import getpass, GetPassWarning


@lru_cache(maxsize=2)
def _load_config():
    """Load ~/.educedb as a dictionary."""
    cfg_path = Path.home() / '.educedb'
    if not cfg_path.exists():
        return None

    with cfg_path.open() as f:
        cfg = json.load(f)

    return cfg


def _get_cfg_val(env_key, config_key):
    """Return a config value from the environment or config file."""
    # Prefer env val
    val = os.getenv(env_key, None)
    if val is not None:
        return val

    # Load config
    cfg = _load_config()
    if cfg is None:
        _load_config.cache_clear()
        return None

    return cfg.get(config_key, None)


def __getattr__(name):
    """Stub to avoid attribute errors on this module"""
    pass


# Default properties #
uri = _get_cfg_val('EDUCEDB_URI', 'uri')
username = _get_cfg_val('EDUCEDB_USER', 'username')
password = _get_cfg_val('EDUCEDB_PASSWORD', 'password')


def request_required():
    """Prompt the user to provide required configuration information."""
    global uri, username, password
    if uri is None:
        uri = prompt('Enter URI: ')

    if username is None:
        username = prompt('Enter username: ')

    if password is None:
        try:
            password = getpass('Enter password: ')
        except GetPassWarning:
            pass
