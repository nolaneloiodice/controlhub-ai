import streamlit as st

from controlhub.action_log_tools import add_action_log
from controlhub.storage import AGENT_TASKS_FILE, TASKS_FILE, load_json, save_json


def update_task_status(tasks, task_index, new_status):
    task = tasks[task_index]
    old_status = task.get("status", "Non défini")
    title = task.get("title", "Mission sans titre")

    tasks[task_index]["status"] = new_status
    save_json(AGENT_TASKS_FILE, tasks)

    add_action_log(
        source="Missions Agents",
        action_type="Changement statut mission",
        title=title,
        details=f"Statut modifié : {old_status} → {new_status}",
    )


def create_task_from_mission(task):
    tasks = load_json(TASKS_FILE, [])

    agent = task.get("agent", "Agent")
    title = task.get("title", "Mission sans titre")
    priority = task.get("priority", "moyenne")
    context = task.get("context", "")

    if "GitHub" in agent:
        category = "GitHub"
    elif "Carrière" in agent:
        category = "Carrière / Alternance"
    elif "Cyber" in agent:
        category = "Cybersécurité"
    elif "Apprentissage" in agent:
        category = "BTS SIO SISR"
    elif "Email" in agent:
        category = "Organisation personnelle"
    elif "LinkedIn" in agent:
        category = "LinkedIn"
    else:
        category = "ControlHub AI"

    task_title = f"Exécuter mission : {title}"

    tasks.append(
        {
            "title": task_title,
            "category": category,
            "priority": priority,
            "status": "à faire",
            "linked_project": "",
            "linked_agent": agent,
            "due_date": "",
            "description": context,
        }
    )

    save_json(TASKS_FILE, tasks)

    add_action_log(
        source="Missions Agents",
        action_type="Création tâche depuis mission",
        title=task_title,
        details=f"Mission source : {title}\nAgent : {agent}\n\nContexte :\n{context}",
    )


def generate_execution_plan(task):
    agent = task.get("agent", "")
    title = task.get("title", "Mission sans titre")
    context = task.get("context", "")

    if "GitHub" in agent:
        return f"""### Plan d’exécution — {title}

1. Lire le contexte de la mission.
2. Identifier le repository ou le projet concerné.
3. Vérifier le nom recommandé du repository.
4. Vérifier la description GitHub proposée.
5. Relire le README généré ou existant.
6. Vérifier qu’aucune donnée personnelle sensible n’est présente.
7. Préparer une checklist de publication.
8. Attendre validation humaine avant toute création ou modification GitHub.

### Points de contrôle

- Le nom du repository est clair.
- La description est professionnelle.
- Le README explique l’objectif du projet.
- Les compétences travaillées sont visibles.
- Le projet est cohérent avec le portfolio.

### Contexte utilisé

{context}
"""

    if "Carrière" in agent:
        return f"""### Plan d’exécution — {title}

1. Lire le contexte de la mission.
2. Identifier l’objectif carrière : CV, alternance, entretien, relance ou LinkedIn.
3. Préparer un brouillon clair.
4. Vérifier le ton professionnel.
5. Adapter le message au destinataire.
6. Relire avant validation humaine.
7. Ne rien envoyer automatiquement.

### Points de contrôle

- Le message est clair.
- Le ton est professionnel.
- Le contenu est adapté à l’alternance BTS SIO SISR.
- Le message valorise les projets et la progression.

### Contexte utilisé

{context}
"""

    if "Apprentissage" in agent:
        return f"""### Plan d’exécution — {title}

1. Identifier le sujet d’apprentissage.
2. Définir une session de 45 à 90 minutes.
3. Préparer les ressources nécessaires.
4. Travailler sur une seule notion.
5. Noter ce qui est compris.
6. Noter ce qui reste flou.
7. Créer une note dans le learning log.
8. Définir la prochaine action.

### Points de contrôle

- La session a un objectif clair.
- Une note est ajoutée après la session.
- Les blocages sont identifiés.
- Une prochaine action est définie.

### Contexte utilisé

{context}
"""

    if "Cyber" in agent:
        return f"""### Plan d’exécution — {title}

1. Identifier le sujet cyber concerné.
2. Vérifier si la mission est défensive, apprentissage ou lab légal.
3. Préparer l’environnement de travail.
4. Lire les consignes ou notes associées.
5. Travailler étape par étape.
6. Noter les commandes, outils ou concepts importants.
7. Résumer en français ce qui a été appris.
8. Ne jamais exécuter d’action offensive hors environnement autorisé.

### Points de contrôle

- Le cadre est légal et contrôlé.
- Les notions sont comprises.
- Les notes sont documentées.
- Les prochaines étapes sont définies.

### Contexte utilisé

{context}
"""

    return f"""### Plan d’exécution — {title}

1. Lire le contexte de la mission.
2. Définir l’objectif concret.
3. Découper la mission en petites étapes.
4. Exécuter ou préparer uniquement ce qui est sûr.
5. Documenter le résultat.
6. Identifier les blocages.
7. Définir la prochaine action.
8. Attendre validation humaine avant toute action externe.

### Contexte utilisé

{context}
"""


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

        st.markdown("### Suivi mission")

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

        st.divider()

        st.markdown("### Transformer en tâche")

        if st.button(
            "Créer une tâche depuis cette mission",
            key=f"{key_prefix}-create-task-{index}",
        ):
            create_task_from_mission(task)
            st.success("Tâche créée dans Tâches / Planning.")

        st.divider()

        st.markdown("### Exécution agent")

        if st.button(
            "Générer un plan d’exécution",
            key=f"{key_prefix}-execution-plan-{index}",
        ):
            plan = generate_execution_plan(task)
            st.session_state[f"{key_prefix}-execution-plan-result-{index}"] = plan

            add_action_log(
                source="Missions Agents",
                action_type="Plan exécution généré",
                title=f"Plan : {title}",
                details=plan,
            )

        plan_key = f"{key_prefix}-execution-plan-result-{index}"

        if plan_key in st.session_state:
            st.markdown(st.session_state[plan_key])

            st.info(
                "Ce plan est une aide à l’exécution. Aucune action externe n’est lancée automatiquement."
            )


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
                mission = {
                    "agent": agent,
                    "title": title.strip(),
                    "priority": priority,
                    "status": status,
                    "context": context.strip(),
                }

                tasks.append(mission)

                save_json(AGENT_TASKS_FILE, tasks)

                add_action_log(
                    source="Missions Agents",
                    action_type="Création mission",
                    title=title.strip(),
                    details=f"Agent : {agent}\nPriorité : {priority}\nStatut : {status}\n\nContexte :\n{context.strip()}",
                )

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