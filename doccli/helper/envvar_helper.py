import os

def is_env_empty(env: str) -> bool:
    value = os.environ.get(env)
    if value is None:
        return True
    return False
    