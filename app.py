import json
from pathlib import Path

import streamlit as st


DATA_DIR = Path("data")
PROFILE_FILE = DATA_DIR / "profile.json"
SKILLS_FILE = DATA_DIR / "skills.json"
PROJECTS_FILE = DATA_DIR / "projects.json"
GOALS_FILE = DATA_DIR / "goals.json"


def load_json(file_path, default_data):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_data


def main():
    st.set_page_config(
        page_title="ControlHub AI",
        page_icon="🧠",
        layout="wide"
    )

    profile = load_json(PROFILE_FILE, {})
    skills = load_json(SKILLS_FILE, [])
    projects = load_json(PROJECTS_FILE, [])
    goals = load_json(GOALS_FILE, [])

    st.title("🧠 ControlHub AI")
    st.write("Ton centre de contrôle personnel pour progresser en IT, réseaux, cybersécurité et IA.")

    name = profile.get("name", "Nolane")
    main_goal = profile.get("main_goal", "Construire un assistant personnel et progresser en IT/cyber.")

    st.subheader(f"Bienvenue, {name}")
    st.info(main_goal)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Compétences suivies", len(skills))

    with col2:
        st.metric("Projets enregistrés", len(projects))

    with col3:
        active_goals = [goal for goal in goals if goal.get("status") != "terminé"]
        st.metric("Objectifs actifs", len(active_goals))

    st.divider()

    left_col, right_col = st.columns(2)

    with left_col:
        st.header("🎯 Objectifs")

        if not goals:
            st.write("Aucun objectif enregistré.")
        else:
            for goal in goals:
                st.markdown(f"### {goal.get('title', 'Objectif sans titre')}")
                st.write(f"**Catégorie :** {goal.get('category', 'Non définie')}")
                st.write(f"**Priorité :** {goal.get('priority', 'Non définie')}")
                st.write(f"**Statut :** {goal.get('status', 'Non défini')}")
                st.write(goal.get("description", ""))

    with right_col:
        st.header("🧩 Compétences")

        if not skills:
            st.write("Aucune compétence enregistrée.")
        else:
            for skill in skills:
                skill_name = skill.get("name", "Compétence")
                level = skill.get("level", 1)
                st.write(f"**{skill_name}** — {level}/5")
                st.progress(level / 5)

    st.divider()

    st.header("🚀 Projets")

    if not projects:
        st.write("Aucun projet enregistré.")
    else:
        for project in projects:
            with st.expander(project.get("name", "Projet sans nom")):
                st.write(f"**Catégorie :** {project.get('category', 'Non définie')}")
                st.write(f"**Statut :** {project.get('status', 'Non défini')}")
                st.write(f"**GitHub :** {project.get('github_url', '')}")
                st.write(project.get("description", ""))

                skills_list = project.get("skills", [])
                if skills_list:
                    st.write("**Compétences liées :**")
                    st.write(", ".join(skills_list))

    st.divider()

    st.header("🔥 Priorité recommandée")

    high_priority_goals = [
        goal for goal in goals
        if goal.get("priority", "").lower() == "haute"
        and goal.get("status") != "terminé"
    ]

    if high_priority_goals:
        goal = high_priority_goals[0]
        st.success(f"Priorité actuelle : {goal.get('title')}")
        st.write(goal.get("description", ""))
    elif goals:
        goal = goals[0]
        st.info(f"Objectif à avancer : {goal.get('title')}")
        st.write(goal.get("description", ""))
    else:
        st.warning("Ajoute un objectif pour que ControlHub AI puisse recommander une priorité.")


if __name__ == "__main__":
    main()