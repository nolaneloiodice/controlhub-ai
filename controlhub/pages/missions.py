import streamlit as st

from controlhub.storage import AGENT_TASKS_FILE, load_json, save_json


def update_task_status(tasks, task_index, new_status):
    tasks[task_index]["status"] = new_status
    save_json(AGENT_TASKS_FILE, tasks)


def render_task_card(tasks, task, index, key_prefix):
    title = task.get("title", "Mission sans titre")
    agent = task.get("agent", "Agent non défini")
    priority = task.get("priority", "Non définie")
    status = task.get("status", "Non défini")
    context = task.get("context", "")

    with st.expander(f"{index + 1}. {title}"):
        st.write(f"**Agent :** {agent}")
        st.write(f"**Priorité :** {priority}")
        st.write(f"**Statut :** {status}")

        st.write("**Contexte / instructions :**")
        st.write(context if context else "Aucun contexte fourni.")

        st.markdown("### Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Passer en cours", key=f"{key_prefix}-start-task-{index}"):
                update_task_status(tasks, index, "en cours")
                st.success("Mission passée en cours.")
                st.rerun()

        with col2:
            if st.button("Marquer terminé", key=f"{key_prefix}-done-task-{index}"):
                update_task_status(tasks, index, "terminé")
                st.success("Mission terminée.")
                st.rerun()

        with col3:
            if st.button("Remettre à faire", key=f"{key_prefix}-todo-task-{index}"):
                update_task_status(tasks, index, "à faire")
                st.success("Mission remise à faire.")
                st.rerun()


def render_missions_page():
    st.title("🧬 Missions Agents")

    st.write(
        "Cette page permet de créer, suivre et piloter les missions confiées aux futurs agents IA. "
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
        priority = st.selectbox("Priorité", ["basse", "moyenne", "haute"])
        status = st.selectbox("Statut", ["à faire", "en cours", "en attente", "terminé"])
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

    st.subheader("Tableau de bord des missions")

    if not tasks:
        st.write("Aucune mission agent enregistrée.")
        return

    todo_tasks = [task for task in tasks if task.get("status") == "à faire"]
    in_progress_tasks = [task for task in tasks if task.get("status") == "en cours"]
    waiting_tasks = [task for task in tasks if task.get("status") == "en attente"]
    done_tasks = [task for task in tasks if task.get("status") == "terminé"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("À faire", len(todo_tasks))

    with col2:
        st.metric("En cours", len(in_progress_tasks))

    with col3:
        st.metric("En attente", len(waiting_tasks))

    with col4:
        st.metric("Terminées", len(done_tasks))

    st.divider()

    tab_todo, tab_progress, tab_waiting, tab_done, tab_all = st.tabs(
        ["À faire", "En cours", "En attente", "Terminées", "Toutes"]
    )

    with tab_todo:
        st.subheader("Missions à faire")
        found = False
        for index, task in enumerate(tasks):
            if task.get("status") == "à faire":
                render_task_card(tasks, task, index, "todo")
                found = True

        if not found:
            st.write("Aucune mission à faire.")

    with tab_progress:
        st.subheader("Missions en cours")
        found = False
        for index, task in enumerate(tasks):
            if task.get("status") == "en cours":
                render_task_card(tasks, task, index, "progress")
                found = True

        if not found:
            st.write("Aucune mission en cours.")

    with tab_waiting:
        st.subheader("Missions en attente")
        found = False
        for index, task in enumerate(tasks):
            if task.get("status") == "en attente":
                render_task_card(tasks, task, index, "waiting")
                found = True

        if not found:
            st.write("Aucune mission en attente.")

    with tab_done:
        st.subheader("Missions terminées")
        found = False
        for index, task in enumerate(tasks):
            if task.get("status") == "terminé":
                render_task_card(tasks, task, index, "done")
                found = True

        if not found:
            st.write("Aucune mission terminée.")

    with tab_all:
        st.subheader("Toutes les missions")
        for index, task in enumerate(tasks):
            render_task_card(tasks, task, index, "all")