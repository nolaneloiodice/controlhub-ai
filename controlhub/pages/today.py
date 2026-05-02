import streamlit as st

from controlhub.ai_tools import generate_ai_response, get_ollama_model, get_ollama_models
from controlhub.storage import (
    AGENT_TASKS_FILE,
    GOALS_FILE,
    PROJECTS_FILE,
    TASKS_FILE,
    load_all_data,
    load_json,
)


def get_priority_score(item):
    priority = item.get("priority", "moyenne")

    if priority == "haute":
        return 3

    if priority == "moyenne":
        return 2

    return 1


def get_open_items(items):
    return [
        item
        for item in items
        if item.get("status") not in ["terminé", "terminée"]
    ]


def format_items_for_prompt(title, items, limit=8):
    lines = [title]

    if not items:
        lines.append("- Aucun élément.")
        return "\n".join(lines)

    sorted_items = sorted(
        items,
        key=get_priority_score,
        reverse=True,
    )

    for item in sorted_items[:limit]:
        lines.append(
            f"- {item.get('title', item.get('name', 'Sans titre'))} "
            f"| priorité : {item.get('priority', 'non définie')} "
            f"| statut : {item.get('status', 'non défini')} "
            f"| description : {item.get('description', item.get('context', ''))}"
        )

    return "\n".join(lines)


def render_today_page():
    profile, skills, projects, goals = load_all_data()

    tasks = load_json(TASKS_FILE, [])
    agent_missions = load_json(AGENT_TASKS_FILE, [])

    open_tasks = get_open_items(tasks)
    open_missions = get_open_items(agent_missions)
    open_goals = get_open_items(goals)

    high_priority_tasks = [
        task for task in open_tasks if task.get("priority") == "haute"
    ]

    high_priority_missions = [
        mission for mission in open_missions if mission.get("priority") == "haute"
    ]

    st.title("📍 Aujourd’hui")

    st.write(
        "Cette page sert à décider rapidement quoi faire maintenant. "
        "Elle combine tes tâches, missions agents, objectifs, projets et l’IA locale."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Tâches ouvertes", len(open_tasks))

    with col2:
        st.metric("Missions ouvertes", len(open_missions))

    with col3:
        st.metric("Objectifs actifs", len(open_goals))

    with col4:
        st.metric(
            "Priorités hautes",
            len(high_priority_tasks) + len(high_priority_missions),
        )

    st.divider()

    st.header("🔥 Priorité immédiate")

    if high_priority_tasks:
        task = high_priority_tasks[0]
        st.success(task.get("title", "Tâche prioritaire"))
        st.write(task.get("description", ""))
    elif high_priority_missions:
        mission = high_priority_missions[0]
        st.success(mission.get("title", "Mission prioritaire"))
        st.write(mission.get("context", ""))
    elif open_tasks:
        task = open_tasks[0]
        st.info(task.get("title", "Tâche à traiter"))
        st.write(task.get("description", ""))
    elif open_missions:
        mission = open_missions[0]
        st.info(mission.get("title", "Mission à traiter"))
        st.write(mission.get("context", ""))
    else:
        st.warning("Aucune tâche ou mission active. Ajoute une tâche ou une mission pour guider ta journée.")

    st.divider()

    st.header("🧭 Vue rapide")

    tab_tasks, tab_missions, tab_goals = st.tabs(
        [
            "Tâches ouvertes",
            "Missions ouvertes",
            "Objectifs actifs",
        ]
    )

    with tab_tasks:
        if not open_tasks:
            st.write("Aucune tâche ouverte.")
        else:
            sorted_tasks = sorted(open_tasks, key=get_priority_score, reverse=True)

            for index, task in enumerate(sorted_tasks[:8], start=1):
                with st.expander(f"{index}. {task.get('title', 'Tâche sans titre')}"):
                    st.write(f"**Priorité :** {task.get('priority', 'Non définie')}")
                    st.write(f"**Statut :** {task.get('status', 'Non défini')}")
                    st.write(f"**Catégorie :** {task.get('category', 'Non définie')}")
                    st.write(task.get("description", ""))

    with tab_missions:
        if not open_missions:
            st.write("Aucune mission ouverte.")
        else:
            sorted_missions = sorted(open_missions, key=get_priority_score, reverse=True)

            for index, mission in enumerate(sorted_missions[:8], start=1):
                with st.expander(f"{index}. {mission.get('title', 'Mission sans titre')}"):
                    st.write(f"**Agent :** {mission.get('agent', 'Non défini')}")
                    st.write(f"**Priorité :** {mission.get('priority', 'Non définie')}")
                    st.write(f"**Statut :** {mission.get('status', 'Non défini')}")
                    st.write(mission.get("context", ""))

    with tab_goals:
        if not open_goals:
            st.write("Aucun objectif actif.")
        else:
            sorted_goals = sorted(open_goals, key=get_priority_score, reverse=True)

            for index, goal in enumerate(sorted_goals[:8], start=1):
                with st.expander(f"{index}. {goal.get('title', 'Objectif sans titre')}"):
                    st.write(f"**Catégorie :** {goal.get('category', 'Non définie')}")
                    st.write(f"**Priorité :** {goal.get('priority', 'Non définie')}")
                    st.write(f"**Statut :** {goal.get('status', 'Non défini')}")
                    st.write(goal.get("description", ""))

    st.divider()

    st.header("🤖 Générer ma journée optimale")

    available_models = get_ollama_models()
    selected_model = None

    if available_models:
        default_model = get_ollama_model()

        if default_model in available_models:
            default_index = available_models.index(default_model)
        else:
            default_index = 0

        selected_model = st.selectbox(
            "Modèle IA local",
            available_models,
            index=default_index,
        )

    session_duration = st.selectbox(
        "Temps disponible aujourd’hui",
        [
            "30 minutes",
            "45 minutes",
            "1 heure",
            "1h30",
            "2 heures",
            "3 heures",
            "Demi-journée",
            "Journée complète",
        ],
    )

    energy_level = st.selectbox(
        "Énergie actuelle",
        [
            "basse",
            "moyenne",
            "haute",
        ],
        index=1,
    )

    focus = st.selectbox(
        "Orientation souhaitée",
        [
            "Avancer efficacement",
            "Apprendre",
            "Produire quelque chose de visible",
            "Préparer GitHub / portfolio",
            "Organisation personnelle",
            "Préparation alternance",
        ],
    )

    if st.button("Générer mon plan optimisé"):
        tasks_context = format_items_for_prompt("Tâches ouvertes :", open_tasks)
        missions_context = format_items_for_prompt("Missions agents ouvertes :", open_missions)
        goals_context = format_items_for_prompt("Objectifs actifs :", open_goals)

        prompt = f"""
Tu dois générer un plan de journée optimisé pour moi.

Contraintes :
- Temps disponible : {session_duration}
- Énergie actuelle : {energy_level}
- Orientation souhaitée : {focus}

Règles :
- Ne propose pas d’outil externe.
- Utilise ControlHub AI comme centre de contrôle.
- Propose un plan réaliste.
- Donne une seule priorité principale.
- Donne une deuxième action optionnelle.
- Termine par une mini-note à écrire dans le learning log.
- Ne propose aucune fonctionnalité inexistante comme si elle existait déjà.

Données disponibles :

{tasks_context}

{missions_context}

{goals_context}

Projets enregistrés :
{format_items_for_prompt("Projets :", projects)}
"""

        with st.spinner("Génération du plan optimisé avec l’IA locale..."):
            result = generate_ai_response(
                prompt,
                profile,
                skills,
                projects,
                goals,
                model_name=selected_model,
            )

        st.subheader("Plan optimisé")
        st.markdown(result)