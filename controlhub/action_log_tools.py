from datetime import datetime

from controlhub.storage import ACTION_LOG_FILE, load_json, save_json


def load_action_log():
    return load_json(ACTION_LOG_FILE, [])


def add_action_log(source, action_type, title, details=""):
    logs = load_action_log()

    logs.insert(
        0,
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": source,
            "action_type": action_type,
            "title": title,
            "details": details,
        },
    )

    save_json(ACTION_LOG_FILE, logs)


def clear_action_log():
    save_json(ACTION_LOG_FILE, [])