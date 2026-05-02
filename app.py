import streamlit as st

from controlhub.pages.command_center import render_command_center_page
from controlhub.pages.github import render_github_page
from controlhub.pages.home import render_home_page
from controlhub.pages.ai_assistant import render_ai_assistant_page
from controlhub.pages.daily_session import render_daily_session_page
from controlhub.pages.roadmap import render_roadmap_page
from controlhub.pages.skills import render_skills_page
from controlhub.pages.projets import render_projects_page
from controlhub.pages.goals import render_goals_page
from controlhub.pages.notes import render_notes_page
from controlhub.pages.missions import render_missions_page
from controlhub.storage import (
    PROFILE_FILE,
    SKILLS_FILE,
    PROJECTS_FILE,
    GOALS_FILE,
    AGENT_TASKS_FILE,
    LEARNING_LOG_FILE,
    load_json,
    save_json,
    load_all_data,
)


def main():
    st.set_page_config(
        page_title="ControlHub AI",
        page_icon="🧠",
        layout="wide"
    )

    st.sidebar.title("🧠 ControlHub AI")
    st.sidebar.write("Bureau de contrôle personnel")

    page = st.sidebar.radio(
    "Navigation",
    [
    "Accueil",
    "Command Center",
    "Missions Agents",
    "GitHub",
    "Compétences",
    "Projets",
    "Objectifs",
    "Roadmap",
    "Session du jour",
    "Notes",
    "Assistant IA"
    ]
)

    st.sidebar.divider()
    st.sidebar.caption("Version 1.1 — GitHub missions")

    if page == "Accueil":
        render_home_page()
    elif page == "Command Center":
        render_command_center_page()
    elif page == "Missions Agents":
        render_missions_page()
    elif page == "GitHub":
        render_github_page()
    elif page == "Compétences":
        render_skills_page()
    elif page == "Projets":
        render_projects_page()
    elif page == "Objectifs":
        render_goals_page()
    elif page == "Roadmap":
        render_roadmap_page()
    elif page == "Session du jour":
        render_daily_session_page()
    elif page == "Notes":
        render_notes_page()
    elif page == "Assistant IA":
        render_ai_assistant_page()

if __name__ == "__main__":
    main()