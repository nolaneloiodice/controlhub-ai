import streamlit as st

from controlhub.pages.action_log import render_action_log_page
from controlhub.pages.ai_assistant import render_ai_assistant_page
from controlhub.pages.command_center import render_command_center_page
from controlhub.pages.daily_session import render_daily_session_page
from controlhub.pages.dev_workshop import render_dev_workshop_page
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


APP_VERSION = "Version 3.1 — Atelier Dev orchestré"


PAGES_BY_SECTION = {
    "Principal": [
        "Pilotage",
        "Aujourd'hui",
        "Command Center",
    ],
    "Organisation": [
        "Tâches / Planning",
        "Missions Agents",
        "Projets",
        "Objectifs",
        "Session du jour",
    ],
    "IA & Agents": [
        "Assistant IA",
        "Atelier Dev IA",
        "Mémoire",
    ],
    "GitHub & Portfolio": [
        "GitHub",
        "Repo Builder",
        "Compétences",
        "Roadmap",
    ],
    "Suivi & Données": [
        "Journal",
        "Notes",
        "Accueil",
    ],
}


PAGE_RENDERERS = {
    "Pilotage": render_pilot_page,
    "Accueil": render_home_page,
    "Aujourd'hui": render_today_page,
    "Command Center": render_command_center_page,
    "Journal": render_action_log_page,
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
    "Atelier Dev IA": render_dev_workshop_page,
}


def get_all_pages():
    pages = []

    for section_pages in PAGES_BY_SECTION.values():
        for page in section_pages:
            if page not in pages:
                pages.append(page)

    return pages


def get_section_for_page(page_name):
    for section_name, pages in PAGES_BY_SECTION.items():
        if page_name in pages:
            return section_name

    return "Principal"


def apply_app_style():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(120, 120, 120, 0.18);
        }

        div[data-testid="stMetric"] {
            background: rgba(120, 120, 120, 0.08);
            border: 1px solid rgba(120, 120, 120, 0.15);
            padding: 0.8rem;
            border-radius: 0.8rem;
        }

        div[data-testid="stExpander"] {
            border-radius: 0.8rem;
            border: 1px solid rgba(120, 120, 120, 0.16);
        }

        .stButton button {
            border-radius: 0.7rem;
            min-height: 2.5rem;
            font-weight: 500;
        }

        .app-header {
            padding: 0.8rem 1rem;
            border-radius: 1rem;
            background: linear-gradient(135deg, rgba(120,120,120,0.12), rgba(120,120,120,0.04));
            border: 1px solid rgba(120,120,120,0.18);
            margin-bottom: 1rem;
        }

        .app-header-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .app-header-subtitle {
            opacity: 0.75;
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    all_pages = get_all_pages()
    section_names = list(PAGES_BY_SECTION.keys())

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Pilotage"

    if "pending_page" in st.session_state:
        pending_page = st.session_state.pop("pending_page")

        if pending_page in all_pages:
            st.session_state["current_page"] = pending_page
            st.session_state["nav_section"] = get_section_for_page(pending_page)
            st.session_state["nav_page"] = pending_page

    if st.session_state["current_page"] not in all_pages:
        st.session_state["current_page"] = "Pilotage"

    current_page = st.session_state["current_page"]
    current_section = get_section_for_page(current_page)

    if st.session_state.get("nav_section") not in section_names:
        st.session_state["nav_section"] = current_section

    st.sidebar.title("🧠 ControlHub AI")
    st.sidebar.caption("Centre de contrôle personnel")

    st.sidebar.divider()

    selected_section = st.sidebar.selectbox(
        "Espace",
        section_names,
        key="nav_section",
    )

    pages = PAGES_BY_SECTION[selected_section]

    if st.session_state.get("nav_page") not in pages:
        if current_page in pages:
            st.session_state["nav_page"] = current_page
        else:
            st.session_state["nav_page"] = pages[0]

    selected_page = st.sidebar.radio(
        "Module",
        pages,
        key="nav_page",
    )

    st.session_state["current_page"] = selected_page

    st.sidebar.divider()

    st.sidebar.markdown("### Raccourcis")

    if st.sidebar.button("🎛️ Pilotage", key="sidebar-shortcut-pilot"):
        st.session_state["pending_page"] = "Pilotage"
        st.rerun()

    if st.sidebar.button("📍 Aujourd'hui", key="sidebar-shortcut-today"):
        st.session_state["pending_page"] = "Aujourd'hui"
        st.rerun()

    if st.sidebar.button("🤖 Assistant IA", key="sidebar-shortcut-ai"):
        st.session_state["pending_page"] = "Assistant IA"
        st.rerun()

    if st.sidebar.button("🛠️ Atelier Dev IA", key="sidebar-shortcut-dev"):
        st.session_state["pending_page"] = "Atelier Dev IA"
        st.rerun()

    st.sidebar.divider()
    st.sidebar.caption(APP_VERSION)

    return selected_page


def render_app_header(page):
    section = get_section_for_page(page)

    st.markdown(
        f"""
        <div class="app-header">
            <div class="app-header-title">{page}</div>
            <div class="app-header-subtitle">Espace : {section}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="ControlHub AI",
        page_icon="🧠",
        layout="wide",
    )

    apply_app_style()

    page = render_sidebar()
    render_app_header(page)

    renderer = PAGE_RENDERERS.get(page)

    if renderer:
        renderer()
    else:
        render_pilot_page()


if __name__ == "__main__":
    main()