import streamlit as st

from controlhub.pages.command_center import render_command_center_page
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


def page_home():
    profile, skills, projects, goals = load_all_data()

    st.title("🧠 ControlHub AI")
    st.write("Centre de contrôle personnel pour progresser en IT, réseaux, cybersécurité et IA.")

    name = profile.get("name", "Nolane")
    main_goal = profile.get("main_goal", "Construire un assistant personnel et progresser en IT/cyber.")

    st.subheader(f"Bienvenue, {name}")
    st.info(main_goal)

    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Compétences", len(skills))

    with col2:
        st.metric("Projets", len(projects))

    with col3:
        st.metric("Objectifs actifs", len(active_goals))

    st.divider()

    st.header("🔥 Priorité recommandée")

    high_priority_goals = [
        goal for goal in goals
        if goal.get("priority", "").lower() == "haute"
        and goal.get("status") != "terminé"
    ]

    if high_priority_goals:
        goal = high_priority_goals[0]
        st.success(goal.get("title", "Objectif prioritaire"))
        st.write(goal.get("description", ""))
    elif active_goals:
        goal = active_goals[0]
        st.info(goal.get("title", "Objectif à avancer"))
        st.write(goal.get("description", ""))
    else:
        st.warning("Aucun objectif actif. Ajoute un objectif pour guider ta progression.")

    st.divider()

    st.header("🧭 Prochaine logique de progression")
    st.write(
        "Pour ton profil BTS SIO SISR, la priorité est de consolider : "
        "**réseaux**, **Linux**, **cybersécurité défensive**, puis **Python/automatisation**."
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
    st.sidebar.caption("Version 0.8 — Missions Agents")

    if page == "Accueil":
        page_home()
    elif page == "Command Center":
        render_command_center_page()
    elif page == "Missions Agents":
        render_missions_page()
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