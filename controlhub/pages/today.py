import streamlit as st

from controlhub.action_log_tools import add_action_log
from controlhub.ai_tools import (
    generate_ai_response,
    get_ollama_models,
    get_recommended_model,
)
from controlhub.storage import (
    AGENT_TASKS_FILE,
    LEARNING_LOG_FILE,
    TASKS_FILE,
    load_all_data,
    load_json,
    save_json,
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


def format_items_for_prompt(title, items, limit=6):
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
        description = item.get("description", item.get("context", ""))

        lines.append(
            f"- {item.get('title', item.get('name', 'Sans titre'))} "
            f"| priorité : {item.get('priority', 'non définie')} "
            f"| statut : {item.get('status', 'non défini')} "
            f"| description : {description[:500]}"
        )

    return "\n".join(lines)


def save_today_plan_to_notes(plan, session_duration, energy_level, focus):
    note = f"""

## Plan optimisé du jour

**Temps disponible :** {session_duration}  
**Énergie :** {energy_level}  
**Orientation :** {focus}

### Plan généré

{plan}
"""

    with open(LEARNING_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(note)

    add_action_log(
        source="Aujourd'hui",
        action_type="Création note",
        title="Plan optimisé enregistré dans Notes",
        details=note,
    )


def create_task_from_today_plan(plan, session_duration, energy_level, focus):
    tasks = load_json(TASKS_FILE, [])

    title = f"Exécuter le plan du jour — {focus}"

    description = f"""Plan généré depuis Aujourd'hui.

Temps disponible : {session_duration}
Énergie : {energy_level}
Orientation : {focus}

Plan :
{plan}
"""

    tasks.append(
        {
            "title": title,
            "category": "Organisation personnelle",
            "priority": "haute",
            "status": "à faire",
            "linked_project": "",
            "linked_agent": "Assistant IA",
            "due_date": "",
            "description": description,
        }
    )

    save_json(TASKS_FILE, tasks)

    add_action_log(
        source="Aujourd'hui",
        action_type="Création tâche",
        title=title,
        details=description,
    )


def create_mission_from_today_plan(plan, session_duration, energy_level, focus):
    missions = load_json(AGENT_TASKS_FILE, [])

    title = f"Superviser le plan du jour — {focus}"

    context = f"""Mission créée depuis Aujourd'hui.

Objectif :
Aider Nolane à suivre et exécuter son plan optimisé du jour.

Temps disponible : {session_duration}
Énergie : {energy_level}
Orientation : {focus}

Plan :
{plan}
"""

    missions.append(
        {
            "agent": "Agent Vie personnelle",
            "title": title,
            "priority": "haute",
            "status": "à faire",
            "context": context,
        }
    )

    save_json(AGENT_TASKS_FILE, missions)

    add_action_log(
        source="Aujourd'hui",
        action_type="Création mission",
        title=title,
        details=context,
    )


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

    st.title("📍 Aujourd'hui")

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
        st.warning(
            "Aucune tâche ou mission active. Ajoute une tâche ou une mission pour guider ta journée."
        )

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
    selected_model_label = "Auto"

    if available_models:
        model_options = ["Auto"] + available_models

        selected_model_choice = st.selectbox(
            "Modèle IA local",
            model_options,
            index=0,
        )

        recommended_model = get_recommended_model(
            task_type="planning",
            available_models=available_models,
        )

        if selected_model_choice == "Auto":
            selected_model = None
            selected_model_label = f"Auto ({recommended_model})"
            st.info(f"Mode Auto : ControlHub utilisera probablement {recommended_model}.")
        else:
            selected_model = selected_model_choice
            selected_model_label = selected_model_choice

    response_style = st.selectbox(
        "Style de réponse",
        [
            "Rapide",
            "Normal",
            "Détaillé",
        ],
        index=0,
    )

    st.caption("Pour le cockpit quotidien, le mode Rapide est recommandé.")

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

    if st.button("Générer mon plan optimisé", key="today-generate-plan"):
        tasks_context = format_items_for_prompt("Tâches ouvertes :", open_tasks)
        missions_context = format_items_for_prompt("Missions agents ouvertes :", open_missions)
        goals_context = format_items_for_prompt("Objectifs actifs :", open_goals)
        projects_context = format_items_for_prompt("Projets :", projects)

        prompt = f"""
Tu dois générer un plan de journée optimisé pour moi.

Modules existants dans ControlHub AI :
- Aujourd'hui
- Tâches / Planning
- Missions Agents
- Projets
- Objectifs
- Notes
- Session du jour
- GitHub
- Repo Builder
- Mémoire
- Assistant IA
- Journal
- Pilotage

Contraintes :
- Temps disponible : {session_duration}
- Énergie actuelle : {energy_level}
- Orientation souhaitée : {focus}

Règles :
- Ne propose pas d’outil externe.
- Utilise ControlHub AI comme centre de contrôle.
- Ne dis pas de créer un module qui existe déjà.
- Propose un plan réaliste.
- Donne une seule priorité principale.
- Donne une deuxième action optionnelle.
- Termine par une mini-note à écrire dans le learning log.
- Ne propose aucune fonctionnalité inexistante comme si elle existait déjà.

Données disponibles :

{tasks_context}

{missions_context}

{goals_context}

{projects_context}
"""

        with st.spinner("Génération du plan optimisé avec l’IA locale..."):
            result = generate_ai_response(
                prompt,
                profile,
                skills,
                projects,
                goals,
                model_name=selected_model,
                task_type="planning",
                response_style=response_style,
            )

        st.session_state["today_last_plan"] = result
        st.session_state["today_last_session_duration"] = session_duration
        st.session_state["today_last_energy_level"] = energy_level
        st.session_state["today_last_focus"] = focus

        add_action_log(
            source="Aujourd'hui",
            action_type="Génération plan quotidien",
            title=f"Plan du jour — {focus}",
            details=(
                f"Modèle : {selected_model_label}\n"
                f"Style : {response_style}\n"
                f"Temps disponible : {session_duration}\n"
                f"Énergie : {energy_level}\n"
                f"Orientation : {focus}\n\n"
                f"Plan :\n{result}"
            ),
        )

    if "today_last_plan" in st.session_state:
        st.divider()

        st.subheader("Plan optimisé")
        st.markdown(st.session_state["today_last_plan"])

        st.divider()

        st.subheader("Actions sur ce plan")

        action_col1, action_col2, action_col3 = st.columns(3)

        with action_col1:
            if st.button("Enregistrer dans Notes", key="today-save-plan-notes"):
                save_today_plan_to_notes(
                    st.session_state["today_last_plan"],
                    st.session_state["today_last_session_duration"],
                    st.session_state["today_last_energy_level"],
                    st.session_state["today_last_focus"],
                )

                st.success("Plan enregistré dans Notes.")

        with action_col2:
            if st.button("Créer une tâche", key="today-create-task"):
                create_task_from_today_plan(
                    st.session_state["today_last_plan"],
                    st.session_state["today_last_session_duration"],
                    st.session_state["today_last_energy_level"],
                    st.session_state["today_last_focus"],
                )

                st.success("Tâche créée dans Tâches / Planning.")

        with action_col3:
            if st.button("Créer une mission agent", key="today-create-mission"):
                create_mission_from_today_plan(
                    st.session_state["today_last_plan"],
                    st.session_state["today_last_session_duration"],
                    st.session_state["today_last_energy_level"],
                    st.session_state["today_last_focus"],
                )

                st.success("Mission créée dans Missions Agents.")