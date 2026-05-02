import json
from pathlib import Path


DATA_DIR = Path("data")
DOCS_DIR = Path("docs")

PROFILE_FILE = DATA_DIR / "profile.json"
SKILLS_FILE = DATA_DIR / "skills.json"
PROJECTS_FILE = DATA_DIR / "projects.json"
GOALS_FILE = DATA_DIR / "goals.json"
AGENT_TASKS_FILE = DATA_DIR / "agent_tasks.json"
MEMORY_FILE = DATA_DIR / "memory.json"
LEARNING_LOG_FILE = DOCS_DIR / "learning-log.md"


def load_json(file_path, default_data):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    return default_data


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_all_data():
    profile = load_json(PROFILE_FILE, {})
    skills = load_json(SKILLS_FILE, [])
    projects = load_json(PROJECTS_FILE, [])
    goals = load_json(GOALS_FILE, [])

    return profile, skills, projects, goals