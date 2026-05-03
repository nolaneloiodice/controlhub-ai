import streamlit as st

from controlhub.action_log_tools import add_action_log
from controlhub.storage import PROJECTS_FILE, TASKS_FILE, load_json, save_json


def update_task_status(tasks, task_index, new_status):
    task = tasks[task_index]
    old_status = task.get("status", "Non défini")
    title = task.get("title", "Tâche sans titre")

    tasks[task_index]["status"] = new_status
    save_json(TASKS_FILE, tasks)

    add_action_log(
        source="Tâches / Planning",
        action_type="Changement statut tâche",
        title=title,
        details=f"Statut modifié : {old_status} → {new_status}",
    )


def create_task(
    title,
    category,
    priority,
    status,
    linked_project,
    linked_agent,
    due_date,
    description,
):
    tasks = load_json(TASKS_FILE, [])

    task = {
        "title": title.strip(),
        "category": category.strip(),
        "priority": priority,
        "status": status,
        "linked_project": linked_project,
        "linked_agent": linked_agent,
        "due_date": due_date.strip(),
        "description": description.strip(),
    }

    tasks.append(task)
    save_json(TASKS_FILE, tasks)

    add_action_log(
        source="Tâches / Planning",
        action_type="Création tâche",
        title=title.strip(),
        details=(
            f"Catégorie : {category}\n"
            f"Priorité : {priority}\n"
            f"Statut : {status}\n"
            f"Projet lié : {linked_project if linked_project else 'Aucun'}\n"
            f"Agent lié : {linked_agent if linked_agent else 'Aucun'}\n"
            f"Date prévue : {due_date if due_date else 'Non définie'}\n\n"
            f"Description :\n{description.strip()}"
        ),
    )


def render_task_card(tasks, task, index, key_prefix):
    title = task.get("title", "Tâche sans titre")
    category = task.get("category", "Non définie")
    priority = task.get("priority", "Non définie")
    status = task.get("status", "Non défini")
    linked_project = task.get("linked_project", "")
    linked_agent = task.get("linked_agent", "")
    due_date = task.get("due_date", "")
    description = task.get("description", "")

    with st.expander(f"{index + 1}. {title}"):
        st.write(f"**Catégorie :** {category}")
        st.write(f"**Priorité :** {priority}")
        st.write(f"**Statut :** {status}")

        if linked_project:
            st.write(f"**Projet lié :** {linked_project}")

        if linked_agent:
            st.write(f"**Agent lié :** {linked_agent}")

        if due_date:
            st.write(f"**Date prévue :** {due_date}")

        st.write("**Description :**")
        st.write(description if description else "Aucune description.")

        st.markdown("### Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Passer en cours", key=f"{key_prefix}-start-task-{index}"):
                update_task_status(tasks, index, "en cours")
                st.success("Tâche passée en cours.")
                st.rerun()

        with col2:
            if st.button("Marquer terminé", key=f"{key_prefix}-done-task-{index}"):
                update_task_status(tasks, index, "terminé")
                st.success("Tâche terminée.")
                st.rerun()

        with col3:
            if st.button("Remettre à faire", key=f"{key_prefix}-todo-task-{index}"):
                update_task_status(tasks, index, "à faire")
                st.success("Tâche remise à faire.")
                st.rerun()


def render_tasks_page():
    st.title("✅ Tâches / Planning")

    st.write(
        "Cette page centralise tes tâches concrètes. "
        "Elle sert à transformer tes objectifs, projets et missions agents en actions quotidiennes."
    )

    tasks = load_json(TASKS_FILE, [])
    projects = load_json(PROJECTS_FILE, [])

    project_names = ["Aucun"] + [
        project.get("name", "Projet sans nom") for project in projects
    ]

    with st.form("add_task_form"):
        st.subheader("Ajouter une tâche")

        title = st.text_input("Titre de la tâche")

        category = st.selectbox(
            "Catégorie",
            [
                "ControlHub AI",
                "GitHub",
                "Linux / Systèmes",
                "Réseaux",
                "Cybersécurité",
                "Python",
                "BTS SIO SISR",
                "Carrière / Alternance",
                "LinkedIn",
                "Organisation personnelle",
                "Autre",
            ],
        )

        priority = st.selectbox(
            "Priorité",
            [
                "basse",
                "moyenne",
                "haute",
            ],
            index=1,
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

        linked_project = st.selectbox("Projet lié", project_names)

        linked_agent = st.selectbox(
            "Agent lié",
            [
                "Aucun",
                "Agent Apprentissage",
                "Agent Carrière",
                "Agent GitHub",
                "Agent LinkedIn",
                "Agent Email",
                "Agent Cyber",
                "Agent Vie personnelle",
                "Agent Automatisation",
                "Assistant IA",
            ],
        )

        due_date = st.text_input("Date prévue", placeholder="Exemple : 2026-05-05")
        description = st.text_area("Description / contexte")

        submitted = st.form_submit_button("Ajouter la tâche")

        if submitted:
            if title.strip():
                create_task(
                    title=title,
                    category=category,
                    priority=priority,
                    status=status,
                    linked_project="" if linked_project == "Aucun" else linked_project,
                    linked_agent="" if linked_agent == "Aucun" else linked_agent,
                    due_date=due_date,
                    description=description,
                )

                st.success("Tâche ajoutée.")
                st.rerun()
            else:
                st.error("Le titre est obligatoire.")

    st.divider()

    st.subheader("Tableau de bord des tâches")

    if not tasks:
        st.info("Aucune tâche enregistrée.")
        return

    todo_tasks = [task for task in tasks if task.get("status") == "à faire"]
    progress_tasks = [task for task in tasks if task.get("status") == "en cours"]
    waiting_tasks = [task for task in tasks if task.get("status") == "en attente"]
    done_tasks = [task for task in tasks if task.get("status") == "terminé"]

    high_priority_tasks = [
        task
        for task in tasks
        if task.get("priority") == "haute" and task.get("status") != "terminé"
    ]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("À faire", len(todo_tasks))

    with col2:
        st.metric("En cours", len(progress_tasks))

    with col3:
        st.metric("En attente", len(waiting_tasks))

    with col4:
        st.metric("Terminées", len(done_tasks))

    with col5:
        st.metric("Priorité haute", len(high_priority_tasks))

    st.divider()

    st.subheader("🔥 Action recommandée")

    if high_priority_tasks:
        task = high_priority_tasks[0]
        st.success(task.get("title", "Tâche prioritaire"))
        st.write(task.get("description", ""))
    elif todo_tasks:
        task = todo_tasks[0]
        st.info(task.get("title", "Tâche à faire"))
        st.write(task.get("description", ""))
    else:
        st.info(
            "Aucune tâche urgente. Tu peux créer une nouvelle tâche depuis tes objectifs ou missions."
        )

    st.divider()

    tab_todo, tab_progress, tab_waiting, tab_done, tab_all = st.tabs(
        [
            "À faire",
            "En cours",
            "En attente",
            "Terminées",
            "Toutes",
        ]
    )

    with tab_todo:
        found = False

        for index, task in enumerate(tasks):
            if task.get("status") == "à faire":
                render_task_card(tasks, task, index, "todo")
                found = True

        if not found:
            st.write("Aucune tâche à faire.")

    with tab_progress:
        found = False

        for index, task in enumerate(tasks):
            if task.get("status") == "en cours":
                render_task_card(tasks, task, index, "progress")
                found = True

        if not found:
            st.write("Aucune tâche en cours.")

    with tab_waiting:
        found = False

        for index, task in enumerate(tasks):
            if task.get("status") == "en attente":
                render_task_card(tasks, task, index, "waiting")
                found = True

        if not found:
            st.write("Aucune tâche en attente.")

    with tab_done:
        found = False

        for index, task in enumerate(tasks):
            if task.get("status") == "terminé":
                render_task_card(tasks, task, index, "done")
                found = True

        if not found:
            st.write("Aucune tâche terminée.")

    with tab_all:
        for index, task in enumerate(tasks):
            render_task_card(tasks, task, index, "all")