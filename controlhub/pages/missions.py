import streamlit as st

from controlhub.storage import AGENT_TASKS_FILE, load_json, save_json


def render_missions_page():
    st.title("🧬 Missions Agents")

    st.write(
        "Cette page permet de créer et suivre les missions confiées aux futurs agents IA. "
        "Pour l’instant, les missions sont suivies localement, sans exécution automatique."
    )

    tasks = load_json(AGENT_TASKS_FILE, [])

    with st.form("add_agent_task_form"):
        st.subheader("Créer une mission agent")

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
                "Agent Automatisation",
            ],
        )

        title = st.text_input("Titre de la mission")

        priority = st.selectbox(
            "Priorité",
            [
                "basse",
                "moyenne",
                "haute",
            ],
        )

        status = st.selectbox(
            "Statut",
            [
                "à faire",
                "en cours",
                "en attente",
                "terminé",
            ],
        )

        context = st.text_area("Contexte / instructions")

        submitted = st.form_submit_button("Ajouter la mission")

        if submitted:
            if title.strip():
                tasks.append(
                    {
                        "agent": agent,
                        "title": title.strip(),
                        "priority": priority,
                        "status": status,
                        "context": context.strip(),
                    }
                )

                save_json(AGENT_TASKS_FILE, tasks)
                st.success("Mission ajoutée.")
                st.rerun()
            else:
                st.error("Le titre de la mission est obligatoire.")

    st.divider()

    st.subheader("Missions enregistrées")

    if not tasks:
        st.write("Aucune mission agent enregistrée.")
        return

    pending_tasks = [task for task in tasks if task.get("status") != "terminé"]
    done_tasks = [task for task in tasks if task.get("status") == "terminé"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Missions actives", len(pending_tasks))

    with col2:
        st.metric("Missions terminées", len(done_tasks))

    for index, task in enumerate(tasks, start=1):
        with st.expander(f"{index}. {task.get('title', 'Mission sans titre')}"):
            st.write(f"**Agent :** {task.get('agent', 'Non défini')}")
            st.write(f"**Priorité :** {task.get('priority', 'Non définie')}")
            st.write(f"**Statut :** {task.get('status', 'Non défini')}")
            st.write("**Contexte :**")
            st.write(task.get("context", ""))