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


APP_VERSION = "Version 3.2 — Interface simplifiée"


MAIN_PAGES = [
    "Pilotage",
    "Aujourd'hui",
    "Assistant IA",
    "Atelier Dev IA",
    "Journal",
]


ADVANCED_PAGES_BY_SECTION = {
    "Organisation": [
        "Tâches / Planning",
        "Missions Agents",
        "Projets",
        "Objectifs",
        "Session du jour",
    ],
    "GitHub & Portfolio": [
        "GitHub",
        "Repo Builder",
        "Compétences",
        "Roadmap",
    ],
    "Données": [
        "Notes",
        "Mémoire",
        "Command Center",
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

    for page in MAIN_PAGES:
        if page not in pages:
            pages.append(page)

    for section_pages in ADVANCED_PAGES_BY_SECTION.values():
        for page in section_pages:
            if page not in pages:
                pages.append(page)

    return pages


def get_page_area(page_name):
    if page_name in MAIN_PAGES:
        return "Principal"

    for section_name, pages in ADVANCED_PAGES_BY_SECTION.items():
        if page_name in pages:
            return section_name

    return "Principal"


def go_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()


def apply_app_style():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.2rem;
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
            border-radius: 0.8rem;
            min-height: 2.5rem;
            font-weight: 500;
            width: 100%;
        }

        .app-header {
            padding: 0.9rem 1rem;
            border-radius: 1rem;
            background: linear-gradient(
                135deg,
                rgba(120,120,120,0.12),
                rgba(120,120,120,0.04)
            );
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

        .sidebar-current {
            padding: 0.7rem;
            border-radius: 0.8rem;
            background: rgba(120,120,120,0.10);
            border: 1px solid rgba(120,120,120,0.16);
            font-size: 0.9rem;
            margin-bottom: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    all_pages = get_all_pages()

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Pilotage"

    if "pending_page" in st.session_state:
        pending_page = st.session_state.pop("pending_page")

        if pending_page in all_pages:
            st.session_state["current_page"] = pending_page

    if st.session_state["current_page"] not in all_pages:
        st.session_state["current_page"] = "Pilotage"

    current_page = st.session_state["current_page"]

    st.sidebar.title("🧠 ControlHub AI")
    st.sidebar.caption("Application personnelle de pilotage")

    st.sidebar.divider()

    st.sidebar.markdown(
        f"""
        <div class="sidebar-current">
            <strong>Module actif</strong><br>
            {current_page}<br>
            <span style="opacity: 0.7;">{get_page_area(current_page)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("### Principal")

    if st.sidebar.button("🎛️ Pilotage", key="nav-main-pilot"):
        go_to_page("Pilotage")

    if st.sidebar.button("📍 Aujourd'hui", key="nav-main-today"):
        go_to_page("Aujourd'hui")

    if st.sidebar.button("🤖 Assistant IA", key="nav-main-ai"):
        go_to_page("Assistant IA")

    if st.sidebar.button("🛠️ Atelier Dev IA", key="nav-main-dev"):
        go_to_page("Atelier Dev IA")

    if st.sidebar.button("📜 Journal", key="nav-main-journal"):
        go_to_page("Journal")

    st.sidebar.divider()

    with st.sidebar.expander("Modules avancés"):
        for section_name, pages in ADVANCED_PAGES_BY_SECTION.items():
            st.markdown(f"**{section_name}**")

            for page in pages:
                if st.button(page, key=f"advanced-nav-{section_name}-{page}"):
                    go_to_page(page)

            st.markdown("---")

    st.sidebar.caption(APP_VERSION)

    return current_page


def render_app_header(page):
    area = get_page_area(page)

    st.markdown(
        f"""
        <div class="app-header">
            <div class="app-header-title">{page}</div>
            <div class="app-header-subtitle">Espace : {area}</div>
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