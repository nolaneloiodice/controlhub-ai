import streamlit as st

from controlhub.storage import (
    AGENT_TASKS_FILE,
    LEARNING_LOG_FILE,
    TASKS_FILE,
    load_json,
    save_json,
)


def go_to_page(page_name):
    st.session_state["pending_page"] = page_name
    st.rerun()


def detect_category(user_request):
    request = user_request.lower()

    if any(word in request for word in ["github", "repo", "repository", "readme", "portfolio"]):
        return "GitHub"

    if any(word in request for word in ["linux", "ubuntu", "apache", "système", "systemctl"]):
        return "Linux / Systèmes"

    if any(word in request for word in ["réseau", "cisco", "vlan", "dhcp", "nat", "packet tracer"]):
        return "Réseaux"

    if any(word in request for word in ["cyber", "tryhackme", "sécurité", "soc", "logs"]):
        return "Cybersécurité"

    if any(word in request for word in ["python", "code", "debug", "streamlit"]):
        return "Python"

    if any(word in request for word in ["entretien", "alternance", "cv", "carrière", "commissariat"]):
        return "Carrière / Alternance"

    if any(word in request for word in ["linkedin", "post"]):
        return "LinkedIn"

    if any(word in request for word in ["organisation", "journée", "planning", "vie"]):
        return "Organisation personnelle"

    return "ControlHub AI"


def detect_agent(user_request):
    request = user_request.lower()

    if any(word in request for word in ["github", "repo", "repository", "readme", "portfolio"]):
        return "Agent GitHub"

    if any(word in request for word in ["entretien", "alternance", "cv", "carrière", "linkedin", "email", "mail"]):
        return "Agent Carrière"

    if any(word in request for word in ["cyber", "tryhackme", "sécurité", "soc"]):
        return "Agent Cyber"

    if any(word in request for word in ["apprendre", "réviser", "comprendre", "cours", "lab"]):
        return "Agent Apprentissage"

    if any(word in request for word in ["automatiser", "script", "workflow"]):
        return "Agent Automatisation"

    return "Agent Vie personnelle"


def detect_priority(user_request):
    request = user_request.lower()

    if any(word in request for word in ["urgent", "important", "priorité", "vite", "maintenant", "aujourd"]):
        return "haute"

    if any(word in request for word in ["plus tard", "un jour", "idée", "pas urgent"]):
        return "basse"

    return "moyenne"


def create_task_from_request(user_request):
    tasks = load_json(TASKS_FILE, [])

    category = detect_category(user_request)
    priority = detect_priority(user_request)
    agent = detect_agent(user_request)

    tasks.append(
        {
            "title": user_request.strip()[:80],
            "category": category,
            "priority": priority,
            "status": "à faire",
            "linked_project": "",
            "linked_agent": agent,
            "due_date": "",
            "description": user_request.strip(),
        }
    )

    save_json(TASKS_FILE, tasks)


def create_mission_from_request(user_request):
    missions = load_json(AGENT_TASKS_FILE, [])

    agent = detect_agent(user_request)
    priority = detect_priority(user_request)

    missions.append(
        {
            "agent": agent,
            "title": f"Traiter demande : {user_request.strip()[:70]}",
            "priority": priority,
            "status": "à faire",
            "context": user_request.strip(),
        }
    )

    save_json(AGENT_TASKS_FILE, missions)


def save_note_from_request(user_request):
    note = f"""

## Note rapide — Pilotage central

{user_request.strip()}
"""

    with open(LEARNING_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(note)


def analyze_request(user_request):
    request = user_request.lower().strip()

    suggestions = []

    def add(page, title, reason, priority=1):
        suggestions.append(
            {
                "page": page,
                "title": title,
                "reason": reason,
                "priority": priority,
            }
        )

    if not request:
        return []

    if any(word in request for word in ["aujourd", "maintenant", "priorité", "quoi faire", "journée", "optimisé"]):
        add(
            "Aujourd'hui",
            "Voir quoi faire maintenant",
            "Ta demande concerne la priorité immédiate ou l’organisation de ta journée.",
            10,
        )

    if any(word in request for word in ["tâche", "task", "planning", "todo", "à faire", "planifier"]):
        add(
            "Tâches / Planning",
            "Gérer tes tâches",
            "Ta demande concerne une action concrète à suivre.",
            9,
        )

    if any(word in request for word in ["mission", "agent", "agents", "exécuter", "plan d’exécution"]):
        add(
            "Missions Agents",
            "Piloter les missions agents",
            "Ta demande concerne les missions confiées aux agents IA.",
            9,
        )

    if any(word in request for word in ["github", "repo", "repository", "readme", "portfolio", "public"]):
        if any(word in request for word in ["créer", "nouveau", "publier", "préparer", "builder"]):
            add(
                "Repo Builder",
                "Préparer un repository GitHub",
                "Ta demande concerne la création ou préparation d’un repo à partir d’un projet.",
                10,
            )
        else:
            add(
                "GitHub",
                "Analyser tes repositories GitHub",
                "Ta demande concerne tes repositories existants, README ou portfolio GitHub.",
                8,
            )

    if any(word in request for word in ["projet", "projects"]):
        add(
            "Projets",
            "Gérer tes projets",
            "Ta demande concerne un projet enregistré dans ControlHub AI.",
            7,
        )

    if any(word in request for word in ["objectif", "objectifs", "but", "priorité long terme"]):
        add(
            "Objectifs",
            "Gérer tes objectifs",
            "Ta demande concerne tes objectifs ou priorités.",
            7,
        )

    if any(word in request for word in ["note", "notes", "résumé", "résumer", "learning log", "mémoriser"]):
        add(
            "Notes",
            "Écrire ou consulter tes notes",
            "Ta demande concerne la mémorisation, les résumés ou le learning log.",
            8,
        )

    if any(word in request for word in ["session", "travailler", "apprendre", "réviser", "lab", "tryhackme"]):
        add(
            "Session du jour",
            "Lancer une session structurée",
            "Ta demande concerne une session de travail ou d’apprentissage.",
            8,
        )

    if any(word in request for word in ["ia", "assistant", "rédige", "écris", "décision", "choix", "optimisé", "aide-moi"]):
        add(
            "Assistant IA",
            "Demander à l’assistant IA",
            "Ta demande nécessite une génération, une analyse ou une aide personnalisée.",
            9,
        )

    if any(word in request for word in ["souviens", "mémoire", "préférence", "retenir", "adapte-toi"]):
        add(
            "Mémoire",
            "Ajouter ou consulter la mémoire",
            "Ta demande concerne ce que ControlHub AI doit retenir sur toi.",
            9,
        )

    if any(word in request for word in ["compétence", "niveau", "skills", "progression"]):
        add(
            "Compétences",
            "Suivre tes compétences",
            "Ta demande concerne tes compétences ou ton niveau.",
            6,
        )

    if any(word in request for word in ["roadmap", "parcours", "chemin", "plan long terme"]):
        add(
            "Roadmap",
            "Voir ta roadmap",
            "Ta demande concerne ta direction globale ou ton plan long terme.",
            6,
        )

    if any(word in request for word in ["linkedin", "email", "mail", "entretien", "alternance", "cv", "carrière"]):
        add(
            "Assistant IA",
            "Préparer un contenu carrière",
            "Ta demande concerne LinkedIn, email, entretien, alternance ou carrière.",
            10,
        )

        add(
            "Missions Agents",
            "Créer une mission carrière",
            "Tu peux transformer cette demande en mission pour l’Agent Carrière.",
            7,
        )

    if not suggestions:
        add(
            "Assistant IA",
            "Analyser ta demande avec l’IA",
            "Je n’ai pas identifié une page précise. L’assistant IA peut analyser ta demande.",
            5,
        )

    suggestions = sorted(
        suggestions,
        key=lambda item: item["priority"],
        reverse=True,
    )

    unique_suggestions = []
    seen_pages = set()

    for suggestion in suggestions:
        if suggestion["page"] not in seen_pages:
            unique_suggestions.append(suggestion)
            seen_pages.add(suggestion["page"])

    return unique_suggestions[:4]


def render_quick_actions():
    st.subheader("⚡ Actions rapides")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Quoi faire maintenant ?", key="quick-go-today"):
            go_to_page("Aujourd'hui")

        if st.button("Créer une tâche", key="quick-go-tasks"):
            go_to_page("Tâches / Planning")

    with col2:
        if st.button("Piloter mes agents", key="quick-go-missions"):
            go_to_page("Missions Agents")

        if st.button("Créer un repo", key="quick-go-repo-builder"):
            go_to_page("Repo Builder")

    with col3:
        if st.button("Demander à l’IA", key="quick-go-ai"):
            go_to_page("Assistant IA")

        if st.button("Écrire une note", key="quick-go-notes"):
            go_to_page("Notes")

    with col4:
        if st.button("Analyser GitHub", key="quick-go-github"):
            go_to_page("GitHub")

        if st.button("Ajouter mémoire", key="quick-go-memory"):
            go_to_page("Mémoire")


def render_pilot_page():
    st.title("🎛️ Pilotage central")

    st.write(
        "Décris ce que tu veux faire, et ControlHub AI t’envoie vers le bon module "
        "ou crée directement une tâche, une mission ou une note."
    )

    st.info(
        "Cette page est ton point central : tu écris ton besoin, puis tu choisis l’action la plus utile."
    )

    st.divider()

    user_request = st.text_area(
        "Que veux-tu faire ?",
        placeholder=(
            "Exemples :\n"
            "- Je veux créer un repo pour mon projet Ubuntu\n"
            "- Je ne sais pas quoi faire aujourd’hui\n"
            "- Je veux préparer un post LinkedIn\n"
            "- Je veux transformer une mission en tâche\n"
            "- Je veux noter ce que j’ai appris"
        ),
        height=150,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        find_module = st.button("Trouver le bon module", key="pilot-find-module")

    with col2:
        create_task = st.button("Créer une tâche", key="pilot-create-task")

    with col3:
        create_mission = st.button("Créer une mission", key="pilot-create-mission")

    with col4:
        save_note = st.button("Enregistrer une note", key="pilot-save-note")

    if find_module:
        suggestions = analyze_request(user_request)

        st.session_state["pilot_suggestions"] = suggestions
        st.session_state["pilot_last_request"] = user_request

    if create_task:
        if user_request.strip():
            create_task_from_request(user_request)
            st.success("Tâche créée dans Tâches / Planning.")
        else:
            st.error("Écris d’abord ta demande.")

    if create_mission:
        if user_request.strip():
            create_mission_from_request(user_request)
            st.success("Mission créée dans Missions Agents.")
        else:
            st.error("Écris d’abord ta demande.")

    if save_note:
        if user_request.strip():
            save_note_from_request(user_request)
            st.success("Note enregistrée dans Notes.")
        else:
            st.error("Écris d’abord ta demande.")

    if "pilot_suggestions" in st.session_state:
        st.subheader("🎯 Modules recommandés")

        suggestions = st.session_state["pilot_suggestions"]

        if not suggestions:
            st.warning("Je n’ai pas trouvé de module adapté.")
        else:
            for index, suggestion in enumerate(suggestions, start=1):
                with st.container():
                    st.markdown(f"### {index}. {suggestion['title']}")
                    st.write(f"**Module :** {suggestion['page']}")
                    st.write(suggestion["reason"])

                    if st.button(
                        f"Aller vers {suggestion['page']}",
                        key=f"go-to-{suggestion['page']}-{index}",
                    ):
                        go_to_page(suggestion["page"])

                    st.divider()

    render_quick_actions()

    st.divider()

    st.subheader("🧠 Prochaine évolution")

    st.write(
        "Plus tard, cette page pourra analyser ta demande avec l’IA locale et exécuter une action contrôlée : "
        "créer une tâche enrichie, préparer une mission agent, générer une note structurée ou ouvrir directement le bon workflow."
    )