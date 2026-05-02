import streamlit as st

from controlhub.storage import (
    AGENT_TASKS_FILE,
    PROJECTS_FILE,
    load_json,
    save_json,
)


def create_project_github_mission(project):
    tasks = load_json(AGENT_TASKS_FILE, [])

    project_name = project.get("name", "Projet sans nom")
    project_category = project.get("category", "Non définie")
    project_description = project.get("description", "")
    project_skills = project.get("skills", [])

    context = f"""Projet : {project_name}
Catégorie : {project_category}

Objectif :
Préparer la création ou l'amélioration d'un repository GitHub pour ce projet.

Description :
{project_description}

Compétences liées :
"""

    for skill in project_skills:
        context += f"- {skill}\n"

    context += """

Actions attendues :
- Proposer un nom de repository propre
- Générer une description courte
- Générer un README adapté
- Proposer une structure de fichiers
- Préparer les étapes pour publier le projet sur GitHub

Important :
Ne rien créer automatiquement sans validation humaine.
"""

    tasks.append(
        {
            "agent": "Agent GitHub",
            "title": f"Préparer repository GitHub pour {project_name}",
            "priority": "haute",
            "status": "à faire",
            "context": context,
        }
    )

    save_json(AGENT_TASKS_FILE, tasks)


def render_projects_page():
    projects = load_json(PROJECTS_FILE, [])

    st.title("🚀 Projets")

    with st.form("add_project_form"):
        st.subheader("Ajouter un projet")

        name = st.text_input("Nom du projet")
        category = st.text_input(
            "Catégorie",
            placeholder="Réseaux, Systèmes, Cyber, Python, IA...",
        )
        status = st.selectbox("Statut", ["idée", "en cours", "terminé", "en pause"])
        github_url = st.text_input("Lien GitHub")
        description = st.text_area("Description courte")
        skills_input = st.text_input("Compétences liées, séparées par des virgules")

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if name.strip():
                skills = [
                    skill.strip()
                    for skill in skills_input.split(",")
                    if skill.strip()
                ]

                projects.append(
                    {
                        "name": name.strip(),
                        "category": category.strip(),
                        "status": status,
                        "github_url": github_url.strip(),
                        "description": description.strip(),
                        "skills": skills,
                    }
                )

                save_json(PROJECTS_FILE, projects)
                st.success("Projet ajouté.")
                st.rerun()
            else:
                st.error("Le nom du projet est obligatoire.")

    st.divider()

    st.subheader("Projets enregistrés")

    if not projects:
        st.write("Aucun projet enregistré.")
        return

    active_projects = [
        project
        for project in projects
        if project.get("status") in ["idée", "en cours", "en pause"]
    ]
    done_projects = [
        project
        for project in projects
        if project.get("status") == "terminé"
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Projets actifs", len(active_projects))

    with col2:
        st.metric("Projets terminés", len(done_projects))

    for index, project in enumerate(projects, start=1):
        project_name = project.get("name", "Projet sans nom")

        with st.expander(f"{index}. {project_name}"):
            st.write(f"**Catégorie :** {project.get('category', 'Non définie')}")
            st.write(f"**Statut :** {project.get('status', 'Non défini')}")
            st.write(f"**GitHub :** {project.get('github_url', '')}")
            st.write(project.get("description", ""))

            skills = project.get("skills", [])

            if skills:
                st.write("**Compétences liées :**")
                st.write(", ".join(skills))

            st.markdown("### Actions projet")

            if st.button(
                "Créer une mission GitHub pour ce projet",
                key=f"project-github-mission-{index}",
            ):
                create_project_github_mission(project)
                st.success("Mission créée pour l’Agent GitHub.")