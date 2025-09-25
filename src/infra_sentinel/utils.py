
import os

def get_env(default="dev"):
    return os.getenv("INFRA_SENTINEL_ENV", default)

def fmt_message(msg: str, variables: dict) -> str:
    try:
        return msg.format(**variables)
    except Exception:
        return msg
