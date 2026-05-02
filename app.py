import streamlit as st

from controlhub.pages.ai_assistant import render_ai_assistant_page
from controlhub.pages.command_center import render_command_center_page
from controlhub.pages.daily_session import render_daily_session_page
from controlhub.pages.github import render_github_page
from controlhub.pages.goals import render_goals_page
from controlhub.pages.home import render_home_page
from controlhub.pages.memory import render_memory_page
from controlhub.pages.missions import render_missions_page
from controlhub.pages.notes import render_notes_page
from controlhub.pages.pilot import render_pilot_page
from controlhub.pages.projects import render_projects_page
from controlhub.pages.repo_builder import render_repo_builder_page
from controlhub.pages.roadmap import render_roadmap_page
from controlhub.pages.skills import render_skills_page
from controlhub.pages.tasks import render_tasks_page
from controlhub.pages.today import render_today_page


PAGES = [
    "Pilotage",
    "Accueil",
    "Aujourd'hui",
    "Command Center",
    "Missions Agents",
    "Tâches / Planning",
    "GitHub",
    "Repo Builder",
    "Compétences",
    "Projets",
    "Objectifs",
    "Roadmap",
    "Session du jour",
    "Notes",
    "Assistant IA",
    "Mémoire",
]


PAGE_RENDERERS = {
    "Pilotage": render_pilot_page,
    "Accueil": render_home_page,
    "Aujourd'hui": render_today_page,
    "Command Center": render_command_center_page,
    "Missions Agents": render_missions_page,
    "Tâches / Planning": render_tasks_page,
    "GitHub": render_github_page,
    "Repo Builder": render_repo_builder_page,
    "Compétences": render_skills_page,
    "Projets": render_projects_page,
    "Objectifs": render_goals_page,
    "Roadmap": render_roadmap_page,
    "Session du jour": render_daily_session_page,
    "Notes": render_notes_page,
    "Assistant IA": render_ai_assistant_page,
    "Mémoire": render_memory_page,
}


def main():
    st.set_page_config(
        page_title="ControlHub AI",
        page_icon="🧠",
        layout="wide",
    )

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Pilotage"

    if "pending_page" in st.session_state:
        st.session_state["current_page"] = st.session_state.pop("pending_page")

    if st.session_state["current_page"] not in PAGES:
        st.session_state["current_page"] = "Pilotage"

    st.sidebar.title("🧠 ControlHub AI")
    st.sidebar.write("Bureau de contrôle personnel")

    st.sidebar.markdown("### Navigation")

    page = st.sidebar.radio(
        "Navigation",
        PAGES,
        key="current_page",
        label_visibility="collapsed",
    )

    st.sidebar.divider()
    st.sidebar.caption("Version 2.1 — Pilotage intelligent")

    renderer = PAGE_RENDERERS.get(page)

    if renderer:
        renderer()
    else:
        render_pilot_page()


if __name__ == "__main__":
    main()