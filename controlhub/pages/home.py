import streamlit as st

from controlhub.storage import load_all_data


def render_home_page():
    profile, skills, projects, goals = load_all_data()

    st.title("🧠 ControlHub AI")
    st.write("Centre de contrôle personnel pour progresser en IT, réseaux, cybersécurité, IA et organisation personnelle.")

    name = profile.get("name", "Nolane")
    main_goal = profile.get(
        "main_goal",
        "Construire un assistant personnel et progresser en IT/cyber."
    )

    st.subheader(f"Bienvenue, {name}")
    st.info(main_goal)

    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]
    active_projects = [
        project for project in projects
        if project.get("status") in ["idée", "en cours", "en pause"]
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Compétences", len(skills))

    with col2:
        st.metric("Projets", len(projects))

    with col3:
        st.metric("Objectifs actifs", len(active_goals))

    with col4:
        st.metric("Projets actifs", len(active_projects))

    st.divider()

    st.header("🔥 Priorité recommandée")

    high_priority_goals = [
        goal for goal in active_goals
        if goal.get("priority", "").lower() == "haute"
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

    st.header("🕹️ Vision ControlHub AI")

    st.write(
        "ControlHub AI évolue vers un panel général personnel capable de centraliser "
        "tes apprentissages, projets, objectifs, notes, missions agents, GitHub, carrière, "
        "emails, LinkedIn et automatisations."
    )

    st.markdown(
        """
### Modules actuels

- **Command Center** : piloter les agents locaux
- **Missions Agents** : suivre les missions confiées aux agents
- **Compétences** : suivre ta progression
- **Projets** : centraliser tes projets
- **Objectifs** : définir tes priorités
- **Roadmap** : garder une direction claire
- **Session du jour** : structurer ton travail
- **Notes** : mémoriser ce que tu apprends
- **Assistant IA** : générer des actions à partir de tes données locales
        """
    )

    st.divider()

    st.header("🧭 Prochaine évolution")

    st.write(
        "Prochaine grande étape : ajouter un premier connecteur réel, probablement GitHub en lecture seule, "
        "pour que ControlHub AI puisse analyser tes repositories et proposer des améliorations."
    )