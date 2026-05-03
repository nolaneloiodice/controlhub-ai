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
    PROJECTS_FILE,
    TASKS_FILE,
    load_all_data,
    load_json,
    save_json,
)


def go_to_page(page_name):
    st.session_state["pending_page"] = page_name
    st.rerun()


def normalize_text(text):
    return text.lower().replace("-", " ").replace("_", " ").strip()


def detect_category(user_request):
    request = normalize_text(user_request)

    if any(word in request for word in ["github", "repo", "repository", "readme", "portfolio"]):
        return "GitHub"

    if any(word in request for word in ["linux", "ubuntu", "apache", "système", "systemctl"]):
        return "Linux / Systèmes"

    if any(word in request for word in ["réseau", "reseau", "cisco", "vlan", "dhcp", "nat", "packet tracer"]):
        return "Réseaux"

    if any(word in request for word in ["cyber", "tryhackme", "sécurité", "securite", "soc", "logs"]):
        return "Cybersécurité"

    if any(word in request for word in ["python", "code", "debug", "streamlit"]):
        return "Python"

    if any(word in request for word in ["entretien", "alternance", "cv", "carrière", "carriere", "commissariat"]):
        return "Carrière / Alternance"

    if any(word in request for word in ["linkedin", "post"]):
        return "LinkedIn"

    if any(word in request for word in ["organisation", "journée", "journee", "planning", "vie"]):
        return "Organisation personnelle"

    return "ControlHub AI"


def detect_agent(user_request):
    request = normalize_text(user_request)

    if any(word in request for word in ["github", "repo", "repository", "readme", "portfolio"]):
        return "Agent GitHub"

    if any(word in request for word in ["entretien", "alternance", "cv", "carrière", "carriere", "linkedin", "email", "mail"]):
        return "Agent Carrière"

    if any(word in request for word in ["cyber", "tryhackme", "sécurité", "securite", "soc"]):
        return "Agent Cyber"

    if any(word in request for word in ["apprendre", "réviser", "reviser", "comprendre", "cours", "lab"]):
        return "Agent Apprentissage"

    if any(word in request for word in ["automatiser", "script", "workflow"]):
        return "Agent Automatisation"

    return "Agent Vie personnelle"


def detect_priority(user_request):
    request = normalize_text(user_request)

    if any(word in request for word in ["urgent", "important", "priorité", "priorite", "vite", "maintenant", "aujourd"]):
        return "haute"

    if any(word in request for word in ["plus tard", "un jour", "idée", "idee", "pas urgent"]):
        return "basse"

    return "moyenne"


def detect_linked_project(user_request):
    projects = load_json(PROJECTS_FILE, [])

    if not projects:
        return ""

    request = normalize_text(user_request)

    best_project_name = ""
    best_score = 0

    for project in projects:
        project_name = project.get("name", "")
        project_category = project.get("category", "")
        project_description = project.get("description", "")

        searchable_text = normalize_text(
            f"{project_name} {project_category} {project_description}"
        )

        score = 0

        project_words = [
            word
            for word in searchable_text.split()
            if len(word) >= 3
        ]

        for word in project_words:
            if word in request:
                score += 1

        direct_keywords = {
            "ubuntu": ["ubuntu", "apache", "linux", "web server"],
            "vlan": ["vlan", "inter vlan", "router on a stick"],
            "cisco": ["cisco", "packet tracer", "router", "switch"],
            "controlhub": ["controlhub", "dashboard", "panel", "assistant"],
        }

        for keyword_group, keywords in direct_keywords.items():
            if keyword_group in searchable_text:
                for keyword in keywords:
                    if keyword in request:
                        score += 3

        if score > best_score:
            best_score = score
            best_project_name = project_name

    if best_score >= 2:
        return best_project_name

    return ""


def build_clean_title(user_request):
    title = user_request.strip()

    if len(title) <= 80:
        return title

    return title[:77].strip() + "..."


def create_task_from_request(user_request, extra_description=""):
    tasks = load_json(TASKS_FILE, [])

    category = detect_category(user_request)
    priority = detect_priority(user_request)
    agent = detect_agent(user_request)
    linked_project = detect_linked_project(user_request)

    description = user_request.strip()

    if extra_description:
        description += f"\n\nAnalyse IA :\n{extra_description.strip()}"

    task_title = build_clean_title(user_request)

    tasks.append(
        {
            "title": task_title,
            "category": category,
            "priority": priority,
            "status": "à faire",
            "linked_project": linked_project,
            "linked_agent": agent,
            "due_date": "",
            "description": description,
        }
    )

    save_json(TASKS_FILE, tasks)

    add_action_log(
        source="Pilotage",
        action_type="Création tâche",
        title=task_title,
        details=description,
    )


def create_mission_from_request(user_request, extra_context=""):
    missions = load_json(AGENT_TASKS_FILE, [])

    agent = detect_agent(user_request)
    priority = detect_priority(user_request)
    linked_project = detect_linked_project(user_request)

    context = user_request.strip()

    if linked_project:
        context += f"\n\nProjet lié détecté : {linked_project}"

    if extra_context:
        context += f"\n\nAnalyse IA :\n{extra_context.strip()}"

    mission_title = f"Traiter demande : {build_clean_title(user_request)}"

    missions.append(
        {
            "agent": agent,
            "title": mission_title,
            "priority": priority,
            "status": "à faire",
            "context": context,
        }
    )

    save_json(AGENT_TASKS_FILE, missions)

    add_action_log(
        source="Pilotage",
        action_type="Création mission",
        title=mission_title,
        details=context,
    )


def save_note_from_request(user_request, extra_content=""):
    linked_project = detect_linked_project(user_request)

    note = f"""

## Note rapide — Pilotage central

{user_request.strip()}
"""

    if linked_project:
        note += f"\n**Projet lié détecté :** {linked_project}\n"

    if extra_content:
        note += f"\n### Analyse IA\n\n{extra_content.strip()}\n"

    with open(LEARNING_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(note)

    add_action_log(
        source="Pilotage",
        action_type="Création note",
        title=f"Note : {build_clean_title(user_request)}",
        details=note,
    )


def analyze_request(user_request):
    request = normalize_text(user_request)

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

    linked_project = detect_linked_project(user_request)

    if linked_project:
        add(
            "Projets",
            f"Voir le projet détecté : {linked_project}",
            "ControlHub AI a détecté un projet existant lié à ta demande.",
            9,
        )

    if any(word in request for word in ["aujourd", "maintenant", "priorité", "priorite", "quoi faire", "journée", "journee", "optimisé", "optimise"]):
        add(
            "Aujourd'hui",
            "Voir quoi faire maintenant",
            "Ta demande concerne la priorité immédiate ou l’organisation de ta journée.",
            10,
        )

    if any(word in request for word in ["tâche", "tache", "task", "planning", "todo", "à faire", "a faire", "planifier"]):
        add(
            "Tâches / Planning",
            "Gérer tes tâches",
            "Ta demande concerne une action concrète à suivre.",
            9,
        )

    if any(word in request for word in ["mission", "agent", "agents", "exécuter", "executer", "plan d’exécution", "plan d execution"]):
        add(
            "Missions Agents",
            "Piloter les missions agents",
            "Ta demande concerne les missions confiées aux agents IA.",
            9,
        )

    if any(word in request for word in ["github", "repo", "repository", "readme", "portfolio", "public"]):
        if any(word in request for word in ["créer", "creer", "nouveau", "publier", "préparer", "preparer", "builder"]):
            add(
                "Repo Builder",
                "Préparer un repository GitHub",
                "Ta demande concerne la création ou la préparation d’un repo à partir d’un projet.",
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

    if any(word in request for word in ["objectif", "objectifs", "but", "priorité long terme", "priorite long terme"]):
        add(
            "Objectifs",
            "Gérer tes objectifs",
            "Ta demande concerne tes objectifs ou priorités.",
            7,
        )

    if any(word in request for word in ["note", "notes", "résumé", "resume", "résumer", "resumer", "learning log", "mémoriser", "memoriser"]):
        add(
            "Notes",
            "Écrire ou consulter tes notes",
            "Ta demande concerne la mémorisation, les résumés ou le learning log.",
            8,
        )

    if any(word in request for word in ["session", "travailler", "apprendre", "réviser", "reviser", "lab", "tryhackme"]):
        add(
            "Session du jour",
            "Lancer une session structurée",
            "Ta demande concerne une session de travail ou d’apprentissage.",
            8,
        )

    if any(word in request for word in ["ia", "assistant", "rédige", "redige", "écris", "ecris", "décision", "decision", "choix", "optimisé", "optimise", "aide moi"]):
        add(
            "Assistant IA",
            "Demander à l’assistant IA",
            "Ta demande nécessite une génération, une analyse ou une aide personnalisée.",
            9,
        )

    if any(word in request for word in ["souviens", "mémoire", "memoire", "préférence", "preference", "retenir", "adapte toi"]):
        add(
            "Mémoire",
            "Ajouter ou consulter la mémoire",
            "Ta demande concerne ce que ControlHub AI doit retenir sur toi.",
            9,
        )

    if any(word in request for word in ["compétence", "competence", "niveau", "skills", "progression"]):
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

    if any(word in request for word in ["linkedin", "email", "mail", "entretien", "alternance", "cv", "carrière", "carriere"]):
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


def build_ai_pilot_prompt(user_request):
    category = detect_category(user_request)
    agent = detect_agent(user_request)
    priority = detect_priority(user_request)
    linked_project = detect_linked_project(user_request)
    suggestions = analyze_request(user_request)

    suggested_modules = ", ".join([item["page"] for item in suggestions])

    return f"""
Analyse cette demande dans le contexte de ControlHub AI :

Demande :
{user_request}

Détection locale actuelle :
- Catégorie : {category}
- Agent recommandé : {agent}
- Priorité : {priority}
- Projet lié détecté : {linked_project if linked_project else "Aucun"}
- Modules suggérés : {suggested_modules if suggested_modules else "Aucun"}

Tu dois répondre avec :

1. Intention comprise
2. Meilleur module à utiliser
3. Action recommandée maintenant
4. Tâche proposée si utile
5. Mission agent proposée si utile
6. Plan rapide en 3 étapes maximum

Règles :
- Ne propose pas d’outil externe.
- Ne dis pas de créer un module qui existe déjà.
- Utilise ControlHub AI comme centre de contrôle.
- Si tu proposes une tâche ou une mission, elle doit être concrète et courte.
- Sois direct et utile.
"""


def run_ai_pilot_analysis(user_request):
    profile, skills, projects, goals = load_all_data()

    available_models = get_ollama_models()
    model_name = get_recommended_model(
        task_type="planning",
        available_models=available_models,
    )

    prompt = build_ai_pilot_prompt(user_request)

    return generate_ai_response(
        prompt,
        profile,
        skills,
        projects,
        goals,
        model_name=model_name,
        task_type="planning",
        response_style="Rapide",
    )


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


def render_detected_context(user_request):
    if not user_request.strip():
        return

    category = detect_category(user_request)
    agent = detect_agent(user_request)
    priority = detect_priority(user_request)
    linked_project = detect_linked_project(user_request)

    st.subheader("🔎 Détection automatique")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Catégorie", category)

    with col2:
        st.metric("Priorité", priority)

    with col3:
        st.metric("Agent", agent)

    with col4:
        st.metric("Projet lié", linked_project if linked_project else "Aucun")


def render_pilot_page():
    st.title("🎛️ Pilotage central")

    st.write(
        "Décris ce que tu veux faire, et ControlHub AI t’envoie vers le bon module, "
        "crée une tâche, une mission, une note, ou analyse ta demande avec l’IA locale."
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

    render_detected_context(user_request)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        find_module = st.button("Trouver le bon module", key="pilot-find-module")

    with col2:
        ai_analysis = st.button("Analyser avec l’IA", key="pilot-ai-analysis")

    with col3:
        create_task = st.button("Créer une tâche", key="pilot-create-task")

    with col4:
        create_mission = st.button("Créer une mission", key="pilot-create-mission")

    with col5:
        save_note = st.button("Enregistrer une note", key="pilot-save-note")

    if find_module:
        suggestions = analyze_request(user_request)

        st.session_state["pilot_suggestions"] = suggestions
        st.session_state["pilot_last_request"] = user_request

    if ai_analysis:
        if user_request.strip():
            with st.spinner("Analyse avec l’IA locale..."):
                analysis = run_ai_pilot_analysis(user_request)

            st.session_state["pilot_ai_analysis"] = analysis
            st.session_state["pilot_ai_request"] = user_request

            add_action_log(
                source="Pilotage",
                action_type="Analyse IA",
                title=f"Analyse : {build_clean_title(user_request)}",
                details=analysis,
            )
        else:
            st.error("Écris d’abord ta demande.")

    if create_task:
        if user_request.strip():
            create_task_from_request(user_request)
            linked_project = detect_linked_project(user_request)

            if linked_project:
                st.success(f"Tâche créée dans Tâches / Planning avec projet lié : {linked_project}.")
            else:
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

    if "pilot_ai_analysis" in st.session_state:
        st.divider()
        st.subheader("🤖 Analyse IA du pilotage")
        st.markdown(st.session_state["pilot_ai_analysis"])

        st.subheader("Actions depuis l’analyse IA")

        action_col1, action_col2, action_col3 = st.columns(3)

        with action_col1:
            if st.button("Créer tâche avec analyse IA", key="pilot-ai-create-task"):
                create_task_from_request(
                    st.session_state["pilot_ai_request"],
                    extra_description=st.session_state["pilot_ai_analysis"],
                )
                st.success("Tâche créée avec l’analyse IA.")

        with action_col2:
            if st.button("Créer mission avec analyse IA", key="pilot-ai-create-mission"):
                create_mission_from_request(
                    st.session_state["pilot_ai_request"],
                    extra_context=st.session_state["pilot_ai_analysis"],
                )
                st.success("Mission créée avec l’analyse IA.")

        with action_col3:
            if st.button("Enregistrer analyse en note", key="pilot-ai-save-note"):
                save_note_from_request(
                    st.session_state["pilot_ai_request"],
                    extra_content=st.session_state["pilot_ai_analysis"],
                )
                st.success("Analyse enregistrée dans Notes.")

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
        "Plus tard, cette page pourra exécuter des workflows plus avancés : "
        "créer plusieurs tâches, générer un plan complet, préparer un repo, rédiger un mail ou organiser automatiquement une journée."
    )