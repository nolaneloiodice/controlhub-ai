import streamlit as st

from controlhub.agents import run_agent_action
from controlhub.storage import AGENT_TASKS_FILE, load_all_data, load_json, save_json


def create_agent_task(agent, title, priority, status, context):
    tasks = load_json(AGENT_TASKS_FILE, [])

    tasks.append(
        {
            "agent": agent,
            "title": title,
            "priority": priority,
            "status": status,
            "context": context,
        }
    )

    save_json(AGENT_TASKS_FILE, tasks)


def render_command_center_page():
    profile, skills, projects, goals = load_all_data()

    st.title("🕹️ Command Center")

    st.write(
        "Le Command Center est le panneau de contrôle des agents IA de ControlHub AI. "
        "Pour l’instant, les agents fonctionnent en mode local/simulation, sans action automatique externe."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        agent = st.selectbox(
            "Agent",
            [
                "Agent Apprentissage",
                "Agent Carrière",
                "Agent GitHub",
                "Agent LinkedIn",
                "Agent Email",
                "Agent Cyber",
                "Agent Vie personnelle",
            ],
        )

    with col2:
        action = st.selectbox(
            "Action",
            [
                "Préparer ma journée",
                "Générer une tâche prioritaire",
                "Résumer ma progression",
                "Préparer un post LinkedIn",
                "Préparer un email de relance",
                "Proposer une amélioration GitHub",
                "Préparer une session TryHackMe",
                "Préparer une session Linux",
                "Créer une checklist",
            ],
        )

    with col3:
        mode = st.selectbox(
            "Mode d’exécution",
            [
                "Suggestion uniquement",
                "Brouillon à valider",
                "Action contrôlée plus tard",
            ],
        )

    st.info(
        f"Agent sélectionné : **{agent}** | Action : **{action}** | Mode : **{mode}**"
    )

    st.divider()

    if st.button("Lancer l’agent"):
        result = run_agent_action(action, profile, skills, projects, goals)

        st.session_state["last_agent"] = agent
        st.session_state["last_action"] = action
        st.session_state["last_mode"] = mode
        st.session_state["last_result"] = result

    if "last_result" in st.session_state:
        st.subheader("Résultat généré")
        st.markdown(st.session_state["last_result"])

        st.divider()

        st.subheader("Créer une mission depuis ce résultat")

        mission_title = st.text_input(
            "Titre de la mission",
            value=st.session_state.get("last_action", "Mission agent"),
        )

        mission_priority = st.selectbox(
            "Priorité de la mission",
            ["basse", "moyenne", "haute"],
            index=1,
        )

        mission_status = st.selectbox(
            "Statut de la mission",
            ["à faire", "en cours", "en attente", "terminé"],
            index=0,
        )

        if st.button("Ajouter aux Missions Agents"):
            create_agent_task(
                agent=st.session_state.get("last_agent", "Agent"),
                title=mission_title,
                priority=mission_priority,
                status=mission_status,
                context=st.session_state.get("last_result", ""),
            )

            st.success("Mission ajoutée dans Missions Agents.")

        st.caption(
            "Aucune action externe n’est exécutée automatiquement. "
            "La mission est enregistrée pour suivi et validation."
        )