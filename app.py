import streamlit as st

from controlhub.pages.command_center import render_command_center_page
from controlhub.pages.notes import render_notes_page
from controlhub.pages.missions import render_missions_page
from controlhub.storage import (
    PROFILE_FILE,
    SKILLS_FILE,
    PROJECTS_FILE,
    GOALS_FILE,
    AGENT_TASKS_FILE,
    LEARNING_LOG_FILE,
    load_json,
    save_json,
    load_all_data,
)


def page_home():
    profile, skills, projects, goals = load_all_data()

    st.title("🧠 ControlHub AI")
    st.write("Centre de contrôle personnel pour progresser en IT, réseaux, cybersécurité et IA.")

    name = profile.get("name", "Nolane")
    main_goal = profile.get("main_goal", "Construire un assistant personnel et progresser en IT/cyber.")

    st.subheader(f"Bienvenue, {name}")
    st.info(main_goal)

    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Compétences", len(skills))

    with col2:
        st.metric("Projets", len(projects))

    with col3:
        st.metric("Objectifs actifs", len(active_goals))

    st.divider()

    st.header("🔥 Priorité recommandée")

    high_priority_goals = [
        goal for goal in goals
        if goal.get("priority", "").lower() == "haute"
        and goal.get("status") != "terminé"
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

    st.header("🧭 Prochaine logique de progression")
    st.write(
        "Pour ton profil BTS SIO SISR, la priorité est de consolider : "
        "**réseaux**, **Linux**, **cybersécurité défensive**, puis **Python/automatisation**."
    )


def page_skills():
    skills = load_json(SKILLS_FILE, [])

    st.title("🧩 Compétences")

    with st.form("add_skill_form"):
        st.subheader("Ajouter une compétence")

        name = st.text_input("Nom de la compétence")
        level = st.slider("Niveau", min_value=1, max_value=5, value=1)

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if name.strip():
                skills.append({
                    "name": name.strip(),
                    "level": level
                })
                save_json(SKILLS_FILE, skills)
                st.success("Compétence ajoutée.")
                st.rerun()
            else:
                st.error("Le nom de la compétence est obligatoire.")

    st.divider()

    st.subheader("Compétences suivies")

    if not skills:
        st.write("Aucune compétence enregistrée.")
    else:
        for skill in skills:
            skill_name = skill.get("name", "Compétence")
            level = skill.get("level", 1)

            st.write(f"**{skill_name}** — {level}/5")
            st.progress(level / 5)


def page_projects():
    projects = load_json(PROJECTS_FILE, [])

    st.title("🚀 Projets")

    with st.form("add_project_form"):
        st.subheader("Ajouter un projet")

        name = st.text_input("Nom du projet")
        category = st.text_input("Catégorie", placeholder="Réseaux, Systèmes, Cyber, Python, IA...")
        status = st.selectbox("Statut", ["idée", "en cours", "terminé", "en pause"])
        github_url = st.text_input("Lien GitHub")
        description = st.text_area("Description courte")
        skills_input = st.text_input("Compétences liées, séparées par des virgules")

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if name.strip():
                skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]

                projects.append({
                    "name": name.strip(),
                    "category": category.strip(),
                    "status": status,
                    "github_url": github_url.strip(),
                    "description": description.strip(),
                    "skills": skills
                })

                save_json(PROJECTS_FILE, projects)
                st.success("Projet ajouté.")
                st.rerun()
            else:
                st.error("Le nom du projet est obligatoire.")

    st.divider()

    st.subheader("Projets enregistrés")

    if not projects:
        st.write("Aucun projet enregistré.")
    else:
        for project in projects:
            with st.expander(project.get("name", "Projet sans nom")):
                st.write(f"**Catégorie :** {project.get('category', 'Non définie')}")
                st.write(f"**Statut :** {project.get('status', 'Non défini')}")
                st.write(f"**GitHub :** {project.get('github_url', '')}")
                st.write(project.get("description", ""))

                skills = project.get("skills", [])
                if skills:
                    st.write("**Compétences liées :**")
                    st.write(", ".join(skills))


def page_goals():
    goals = load_json(GOALS_FILE, [])

    st.title("🎯 Objectifs")

    with st.form("add_goal_form"):
        st.subheader("Ajouter un objectif")

        title = st.text_input("Titre de l'objectif")
        category = st.text_input("Catégorie", placeholder="Systèmes, Réseaux, Cyber, Python, Portfolio...")
        priority = st.selectbox("Priorité", ["basse", "moyenne", "haute"])
        status = st.selectbox("Statut", ["en cours", "terminé", "en pause"])
        description = st.text_area("Description courte")

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if title.strip():
                goals.append({
                    "title": title.strip(),
                    "category": category.strip(),
                    "priority": priority,
                    "status": status,
                    "description": description.strip()
                })

                save_json(GOALS_FILE, goals)
                st.success("Objectif ajouté.")
                st.rerun()
            else:
                st.error("Le titre de l'objectif est obligatoire.")

    st.divider()

    st.subheader("Objectifs enregistrés")

    if not goals:
        st.write("Aucun objectif enregistré.")
    else:
        for goal in goals:
            with st.expander(goal.get("title", "Objectif sans titre")):
                st.write(f"**Catégorie :** {goal.get('category', 'Non définie')}")
                st.write(f"**Priorité :** {goal.get('priority', 'Non définie')}")
                st.write(f"**Statut :** {goal.get('status', 'Non défini')}")
                st.write(goal.get("description", ""))


def page_roadmap():
    st.title("🧭 Roadmap")

    st.write(
        "Cette roadmap sert à structurer ta progression vers le BTS SIO SISR, "
        "les systèmes, réseaux, cybersécurité et l’automatisation avec Python/IA."
    )

    roadmap = [
        {
            "phase": "Phase 1 — Fondations",
            "status": "en cours",
            "tasks": [
                "Consolider Git/GitHub",
                "Continuer ControlHub AI",
                "Documenter les apprentissages dans le learning log",
                "Organiser les projets existants"
            ]
        },
        {
            "phase": "Phase 2 — Réseaux",
            "status": "en cours",
            "tasks": [
                "Améliorer les README des labs Cisco Packet Tracer",
                "Revoir IP, masque, passerelle, DNS, DHCP",
                "Revoir VLAN, routage inter-VLAN et NAT/PAT",
                "Ajouter un lab ACL si nécessaire"
            ]
        },
        {
            "phase": "Phase 3 — Linux / Systèmes",
            "status": "à reprendre",
            "tasks": [
                "Reprendre la VM Ubuntu",
                "Diagnostiquer Apache",
                "Comprendre systemctl, services, ports et pare-feu",
                "Créer un mini-projet GitHub Ubuntu Web Server Lab"
            ]
        },
        {
            "phase": "Phase 4 — Cybersécurité défensive",
            "status": "commencé",
            "tasks": [
                "Continuer TryHackMe",
                "Résumer chaque room importante",
                "Comprendre logs, détection, durcissement et bonnes pratiques",
                "Créer des notes cyber en français"
            ]
        },
        {
            "phase": "Phase 5 — Portfolio professionnel",
            "status": "en cours",
            "tasks": [
                "Rendre GitHub plus lisible",
                "Ajouter des descriptions propres aux projets",
                "Préparer des posts LinkedIn",
                "Préparer le pitch alternance BTS SIO SISR"
            ]
        },
        {
            "phase": "Phase 6 — IA / Automatisation",
            "status": "en construction",
            "tasks": [
                "Améliorer le dashboard ControlHub AI",
                "Ajouter une vraie génération de tâches",
                "Ajouter une page notes",
                "Connecter une IA plus tard"
            ]
        }
    ]

    for item in roadmap:
        with st.expander(f"{item['phase']} — {item['status']}"):
            for task in item["tasks"]:
                st.checkbox(task, value=False)

    st.divider()

    st.header("🔥 Prochaine action recommandée")

    st.success("Reprendre le lab Ubuntu Apache")
    st.write(
        "C’est une bonne priorité car elle relie Linux, réseau, services système, "
        "diagnostic et cybersécurité de base."
    )

    st.markdown("### Plan rapide")
    st.write("1. Démarrer la VM Ubuntu")
    st.write("2. Vérifier si Apache est installé")
    st.write("3. Vérifier le statut du service Apache")
    st.write("4. Vérifier le port 80")
    st.write("5. Tester dans le navigateur")
    st.write("6. Noter le résultat dans le learning log")


def page_notes():
    st.title("📝 Notes / Learning Log")

    st.write(
        "Cette page te permet de consulter et d’ajouter des notes d’apprentissage "
        "pour Linux, réseaux, cybersécurité, TryHackMe, Python ou tes projets."
    )

    current_log = ""

    if LEARNING_LOG_FILE.exists():
        with open(LEARNING_LOG_FILE, "r", encoding="utf-8") as file:
            current_log = file.read()

    with st.form("add_note_form"):
        st.subheader("Ajouter une note")

        topic = st.selectbox(
            "Sujet",
            [
                "Linux",
                "Réseaux",
                "Cybersécurité",
                "TryHackMe",
                "Python",
                "Git/GitHub",
                "ControlHub AI",
                "Entretien / alternance",
                "Autre"
            ]
        )

        title = st.text_input("Titre de la note")
        content = st.text_area("Contenu de la note")

        submitted = st.form_submit_button("Ajouter au learning log")

        if submitted:
            if title.strip() and content.strip():
                note = (
                    f"\n\n## {title.strip()}\n\n"
                    f"**Sujet :** {topic}\n\n"
                    f"{content.strip()}\n"
                )

                with open(LEARNING_LOG_FILE, "a", encoding="utf-8") as file:
                    file.write(note)

                st.success("Note ajoutée au learning log.")
                st.rerun()
            else:
                st.error("Le titre et le contenu sont obligatoires.")

    st.divider()

    st.subheader("Learning log actuel")

    if current_log.strip():
        st.markdown(current_log)
    else:
        st.write("Aucune note pour le moment.")


def page_daily_session():
    profile, skills, projects, goals = load_all_data()

    st.title("⚡ Session du jour")

    st.write(
        "Cette page sert à structurer une session de travail et à enregistrer automatiquement "
        "un résumé dans ton learning log."
    )

    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]

    goal_titles = [goal.get("title", "Objectif sans titre") for goal in active_goals]

    with st.form("daily_session_form"):
        st.subheader("Préparer ma session")

        if goal_titles:
            selected_goal = st.selectbox("Objectif travaillé", goal_titles)
        else:
            selected_goal = st.text_input("Objectif travaillé", placeholder="Exemple : Reprendre le lab Ubuntu Apache")

        session_type = st.selectbox(
            "Type de session",
            [
                "Linux / Systèmes",
                "Réseaux",
                "Cybersécurité",
                "TryHackMe",
                "Python",
                "Git/GitHub",
                "ControlHub AI",
                "Portfolio / LinkedIn",
                "Autre"
            ]
        )

        duration = st.selectbox(
            "Durée prévue",
            [
                "30 minutes",
                "45 minutes",
                "1 heure",
                "1h30",
                "2 heures",
                "3 heures"
            ]
        )

        done = st.text_area("Ce que j’ai fait")
        understood = st.text_area("Ce que j’ai compris")
        blockers = st.text_area("Ce qui bloque encore")
        next_action = st.text_area("Prochaine action")

        submitted = st.form_submit_button("Enregistrer la session")

        if submitted:
            if selected_goal.strip() and done.strip():
                note = f"""

## Session du jour — {selected_goal.strip()}

**Type :** {session_type}  
**Durée :** {duration}

### Ce que j’ai fait

{done.strip()}

### Ce que j’ai compris

{understood.strip() if understood.strip() else "À compléter."}

### Ce qui bloque encore

{blockers.strip() if blockers.strip() else "Aucun blocage noté."}

### Prochaine action

{next_action.strip() if next_action.strip() else "À définir."}
"""

                with open(LEARNING_LOG_FILE, "a", encoding="utf-8") as file:
                    file.write(note)

                st.success("Session enregistrée dans le learning log.")
                st.rerun()
            else:
                st.error("Indique au minimum l’objectif travaillé et ce que tu as fait.")

    st.divider()

    st.subheader("Conseil de session")

    st.info(
        "Travaille sur une seule chose à la fois. À la fin de chaque session, note ce que tu as compris "
        "et ce qui reste flou. C’est ce qui transforme la pratique en progression réelle."
    )


def page_agent_missions():
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
                "Agent Automatisation"
            ]
        )

        title = st.text_input("Titre de la mission")

        priority = st.selectbox(
            "Priorité",
            [
                "basse",
                "moyenne",
                "haute"
            ]
        )

        status = st.selectbox(
            "Statut",
            [
                "à faire",
                "en cours",
                "en attente",
                "terminé"
            ]
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
                        "context": context.strip()
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

    st.metric("Missions actives", len(pending_tasks))

    for index, task in enumerate(tasks, start=1):
        with st.expander(f"{index}. {task.get('title', 'Mission sans titre')}"):
            st.write(f"**Agent :** {task.get('agent', 'Non défini')}")
            st.write(f"**Priorité :** {task.get('priority', 'Non définie')}")
            st.write(f"**Statut :** {task.get('status', 'Non défini')}")
            st.write("**Contexte :**")
            st.write(task.get("context", ""))

    if done_tasks:
        st.success(f"{len(done_tasks)} mission(s) terminée(s).")


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


def page_command_center():
    profile, skills, projects, goals = load_all_data()

    st.title("🕹️ Command Center")

    st.write(
        "Le Command Center est le futur panneau de contrôle des agents IA de ControlHub AI. "
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
                "Agent Vie personnelle"
            ]
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
                "Créer une checklist"
            ]
        )

    with col3:
        mode = st.selectbox(
            "Mode d’exécution",
            [
                "Suggestion uniquement",
                "Brouillon à valider",
                "Action contrôlée plus tard"
            ]
        )

    st.info(
        f"Agent sélectionné : **{agent}** | Action : **{action}** | Mode : **{mode}**"
    )

    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]
    high_priority_goals = [
        goal for goal in active_goals
        if goal.get("priority", "").lower() == "haute"
    ]

    priority_goal = None

    if high_priority_goals:
        priority_goal = high_priority_goals[0]
    elif active_goals:
        priority_goal = active_goals[0]

    st.divider()

    if st.button("Lancer l’agent"):
        st.subheader("Résultat généré")

        if action == "Préparer ma journée":
            st.markdown("### Plan de journée recommandé")

            if priority_goal:
                st.write(f"**Priorité principale :** {priority_goal.get('title')}")
                st.write(priority_goal.get("description", ""))

            st.write("1. Faire une session concentrée de 45 à 90 minutes.")
            st.write("2. Travailler sur une seule priorité.")
            st.write("3. Noter ce qui a été fait dans le learning log.")
            st.write("4. Faire un petit commit Git si le projet a avancé.")
            st.write("5. Préparer la prochaine action.")

        elif action == "Générer une tâche prioritaire":
            if priority_goal:
                st.success(priority_goal.get("title", "Objectif prioritaire"))
                st.write(priority_goal.get("description", ""))

                st.markdown("### Tâche concrète")
                st.write(
                    "Travaille 60 minutes sur cet objectif. À la fin, écris une note courte avec : "
                    "ce que tu as fait, ce que tu as compris, ce qui bloque, prochaine action."
                )
            else:
                st.warning("Aucun objectif actif trouvé. Ajoute un objectif dans l’onglet Objectifs.")

        elif action == "Résumer ma progression":
            name = profile.get("name", "Nolane")
            main_goal = profile.get("main_goal", "progresser en IT/cyber")

            st.markdown("### Résumé de progression")

            st.write(f"**Profil :** {name}")
            st.write(f"**Objectif principal :** {main_goal}")
            st.write(f"**Compétences suivies :** {len(skills)}")
            st.write(f"**Projets enregistrés :** {len(projects)}")
            st.write(f"**Objectifs actifs :** {len(active_goals)}")

            if projects:
                st.markdown("### Projets clés")
                for project in projects[:5]:
                    st.write(
                        f"- **{project.get('name', 'Projet')}** "
                        f"({project.get('category', 'Catégorie non définie')})"
                    )

        elif action == "Préparer un post LinkedIn":
            st.markdown("### Brouillon LinkedIn")

            st.markdown(
                """
Je continue à construire **ControlHub AI**, mon centre de contrôle personnel pour organiser ma progression en informatique.

L’objectif est de centraliser mes compétences, mes projets, mes objectifs, mes notes et mes prochaines actions dans un dashboard Python.

Ce projet me permet d’apprendre en construisant, tout en renforçant des compétences importantes pour mon parcours BTS SIO SISR :
- systèmes et réseaux
- Linux
- cybersécurité
- Python
- Git/GitHub
- documentation technique
- organisation de projet

Prochaine étape : faire évoluer ControlHub AI vers un véritable panel multi-agents capable de m’assister sur GitHub, les emails, LinkedIn, l’apprentissage et l’organisation quotidienne.
                """
            )

        elif action == "Préparer un email de relance":
            st.markdown("### Brouillon email")

            st.markdown(
                """
Bonjour,

Je me permets de revenir vers vous à la suite de notre échange concernant ma recherche d’alternance pour le BTS SIO option SISR.

Depuis notre rencontre, j’ai continué à structurer ma montée en compétences en systèmes, réseaux et cybersécurité. J’ai notamment avancé sur mes labs réseaux documentés sur GitHub et sur un projet personnel en Python, ControlHub AI, qui me permet de suivre mes compétences, projets, objectifs et notes d’apprentissage.

Je reste disponible pour un entretien ou tout échange complémentaire.

Cordialement,  
Nolane Loiodice
                """
            )

        elif action == "Proposer une amélioration GitHub":
            st.markdown("### Améliorations GitHub recommandées")

            st.write("1. Ajouter une description claire à chaque repository.")
            st.write("2. Améliorer les README avec : objectif, topologie, notions, étapes, résultat.")
            st.write("3. Ajouter des captures ou schémas quand c’est possible.")
            st.write("4. Ajouter une section “Compétences travaillées”.")
            st.write("5. Mettre en avant ControlHub AI comme projet central.")

        elif action == "Préparer une session TryHackMe":
            st.markdown("### Session TryHackMe recommandée")

            st.write("Durée : 45 à 60 minutes.")
            st.write("Objectif : avancer sur une room sans chercher à tout finir trop vite.")
            st.write("Méthode :")
            st.write("1. Lire les consignes en anglais.")
            st.write("2. Noter les mots techniques inconnus.")
            st.write("3. Répondre aux questions.")
            st.write("4. Faire un résumé en français dans Notes.")
            st.write("5. Ajouter les compétences vues dans ControlHub AI.")

        elif action == "Préparer une session Linux":
            st.markdown("### Session Linux recommandée")

            st.write("Objectif : reprendre le lab Ubuntu / Apache.")
            st.write("Plan :")
            st.code(
                """sudo apt update
sudo apt install apache2
systemctl status apache2
ss -tuln
hostname -I""",
                language="bash"
            )
            st.write("À la fin, note ce qui fonctionne et ce qui bloque encore.")

        elif action == "Créer une checklist":
            st.markdown("### Checklist générée")

            st.checkbox("Définir l’objectif de la session")
            st.checkbox("Ouvrir les bons outils")
            st.checkbox("Travailler 45 à 90 minutes")
            st.checkbox("Noter les résultats")
            st.checkbox("Faire un commit si nécessaire")
            st.checkbox("Préparer la prochaine action")

        st.divider()

        st.caption(
            "Pour l’instant, aucune action externe n’est exécutée automatiquement. "
            "Les agents préparent des suggestions et brouillons que tu valides toi-même."
        )


def page_ai_assistant():
    profile, skills, projects, goals = load_all_data()

    st.title("🤖 Assistant IA")

    st.write(
        "Cette page simule un assistant intelligent basé sur tes données locales. "
        "Plus tard, on pourra connecter une vraie IA pour générer des réponses plus avancées."
    )

    st.divider()

    action = st.selectbox(
        "Que veux-tu générer ?",
        [
            "Tâche du jour",
            "Résumé de progression",
            "Idée de post LinkedIn",
            "Action pour l’objectif prioritaire"
        ]
    )

    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]

    high_priority_goals = [
        goal for goal in active_goals
        if goal.get("priority", "").lower() == "haute"
    ]

    priority_goal = None

    if high_priority_goals:
        priority_goal = high_priority_goals[0]
    elif active_goals:
        priority_goal = active_goals[0]

    if st.button("Générer"):
        if action == "Tâche du jour":
            st.subheader("✅ Tâche du jour")

            if priority_goal:
                st.success(priority_goal.get("title", "Objectif prioritaire"))
                st.write(
                    f"Travaille 45 à 60 minutes sur cet objectif : "
                    f"**{priority_goal.get('title', '')}**."
                )
                st.write(priority_goal.get("description", ""))

                st.markdown("### Plan d’action")
                st.write("1. Prépare ton environnement de travail.")
                st.write("2. Travaille sur une seule action concrète.")
                st.write("3. Note ce que tu as compris.")
                st.write("4. Note ce qui bloque encore.")
                st.write("5. Ajoute un court résumé dans l’onglet Notes.")

            elif skills:
                weakest_skill = min(skills, key=lambda skill: skill.get("level", 1))
                st.info(f"Compétence à renforcer : {weakest_skill.get('name', 'Compétence')}")
                st.write("Travaille 30 à 45 minutes sur cette compétence, puis ajoute une note.")
            else:
                st.warning("Ajoute d’abord des objectifs ou compétences pour générer une tâche pertinente.")

        elif action == "Résumé de progression":
            st.subheader("📈 Résumé de progression")

            name = profile.get("name", "Nolane")
            main_goal = profile.get("main_goal", "progresser en IT, réseaux et cybersécurité")

            st.write(f"**Profil :** {name}")
            st.write(f"**Objectif principal :** {main_goal}")

            st.write(f"Tu suis actuellement **{len(skills)} compétence(s)**, **{len(projects)} projet(s)** et **{len(active_goals)} objectif(s) actif(s)**.")

            if projects:
                st.markdown("### Projets importants")
                for project in projects[:5]:
                    st.write(f"- **{project.get('name', 'Projet')}** — {project.get('category', 'Catégorie non définie')}")

            if active_goals:
                st.markdown("### Objectifs actifs")
                for goal in active_goals:
                    st.write(f"- **{goal.get('title', 'Objectif')}** — priorité {goal.get('priority', 'non définie')}")

        elif action == "Idée de post LinkedIn":
            st.subheader("💼 Idée de post LinkedIn")

            st.markdown(
                """
Aujourd’hui, je continue à structurer ma progression en systèmes, réseaux et cybersécurité autour d’un projet personnel : **ControlHub AI**.

L’objectif est de construire un tableau de bord personnel en Python pour suivre mes compétences, mes projets, mes objectifs et mes notes d’apprentissage.

Ce projet me permet d’apprendre en construisant, tout en renforçant des compétences utiles pour mon parcours BTS SIO SISR :
- Python
- Git/GitHub
- documentation technique
- réseaux
- Linux
- cybersécurité
- organisation de projet

Prochaine étape : améliorer progressivement l’assistant pour générer des tâches, résumés et actions personnalisées à partir de mes données locales.
                """
            )

            st.info("Tu peux copier ce texte, l’adapter, puis le publier quand ton GitHub est bien propre.")

        elif action == "Action pour l’objectif prioritaire":
            st.subheader("🎯 Action recommandée")

            if priority_goal:
                st.success(priority_goal.get("title", "Objectif prioritaire"))
                st.write(priority_goal.get("description", ""))

                st.markdown("### Action concrète")
                st.write(
                    "Fais une session de 45 minutes uniquement sur cet objectif. "
                    "À la fin, écris une note avec : ce que tu as fait, ce que tu as compris, ce qui reste flou."
                )

                st.markdown("### Format de note conseillé")
                st.code(
                    """## Session — Objectif prioritaire

Sujet :
Ce que j’ai fait :
Ce que j’ai compris :
Ce qui bloque :
Prochaine action :
""",
                    language="markdown"
                )
            else:
                st.warning("Aucun objectif actif trouvé. Ajoute un objectif dans l’onglet Objectifs.")


def main():
    st.set_page_config(
        page_title="ControlHub AI",
        page_icon="🧠",
        layout="wide"
    )

    st.sidebar.title("🧠 ControlHub AI")
    st.sidebar.write("Bureau de contrôle personnel")

    page = st.sidebar.radio(
    "Navigation",
    [
    "Accueil",
    "Command Center",
    "Missions Agents",
    "Compétences",
    "Projets",
    "Objectifs",
    "Roadmap",
    "Session du jour",
    "Notes",
    "Assistant IA"
    ]
)

    st.sidebar.divider()
    st.sidebar.caption("Version 0.8 — Missions Agents")

    if page == "Accueil":
        page_home()
    elif page == "Command Center":
        render_command_center_page()
    elif page == "Missions Agents":
        render_missions_page()
    elif page == "Compétences":
        page_skills()
    elif page == "Projets":
        page_projects()
    elif page == "Objectifs":
        page_goals()
    elif page == "Roadmap":
        page_roadmap()
    elif page == "Session du jour":
        page_daily_session()
    elif page == "Notes":
        render_notes_page()
    elif page == "Assistant IA":
        page_ai_assistant()

if __name__ == "__main__":
    main()