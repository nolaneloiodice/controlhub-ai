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


CONTROLHUB_MODULES = """
Modules existants dans ControlHub AI :
- app.py : routeur principal Streamlit
- controlhub/pages/pilot.py : pilotage central
- controlhub/pages/today.py : cockpit quotidien
- controlhub/pages/ai_assistant.py : assistant IA local
- controlhub/pages/missions.py : missions agents
- controlhub/pages/tasks.py : tâches / planning
- controlhub/pages/action_log.py : journal d'activité
- controlhub/pages/memory.py : mémoire locale
- controlhub/pages/github.py : connecteur GitHub lecture seule
- controlhub/pages/repo_builder.py : préparation de repositories GitHub
- controlhub/pages/projects.py : gestion des projets
- controlhub/pages/goals.py : gestion des objectifs
- controlhub/pages/notes.py : notes / learning log
- controlhub/pages/daily_session.py : session du jour
- controlhub/ai_tools.py : couche IA locale Ollama / OpenAI optionnel
- controlhub/action_log_tools.py : journalisation
- controlhub/storage.py : chemins fichiers et JSON
- controlhub/memory_tools.py : mémoire personnelle locale
"""


DEV_AGENT_RULES = """
Règles strictes de l'Agent Développeur ControlHub :
- Ne jamais prétendre avoir modifié un fichier si tu proposes seulement une modification.
- Ne jamais inventer une fonctionnalité existante.
- Toujours distinguer : ce qui existe déjà, ce qui est proposé, ce qui doit être vérifié.
- Toujours citer les fichiers probablement concernés.
- Toujours expliquer l'impact exact sur ControlHub AI.
- Toujours signaler les risques possibles : bugs Streamlit, clés dupliquées, JSON, navigation, imports, données privées.
- Ne jamais chercher sur Internet.
- Si une information externe est nécessaire, demander à Nolane de la fournir.
- Ne jamais proposer d'action irréversible sans sauvegarde.
- Préférer les fichiers complets à remplacer quand c'est plus sûr.
- Répondre en français, de manière claire, directe et actionnable.
"""


def build_dev_prompt(request, request_type, external_context):
    return f"""
Tu es l'Agent Développeur ControlHub.

Ta mission est d'aider Nolane à faire évoluer ControlHub AI lui-même, sous supervision humaine.

Demande de Nolane :
{request}

Type de demande :
{request_type}

Contexte externe fourni par Nolane :
{external_context if external_context.strip() else "Aucun contexte externe fourni."}

{CONTROLHUB_MODULES}

{DEV_AGENT_RULES}

Tu dois répondre avec cette structure :

## 1. Reformulation claire
Explique ce que tu as compris.

## 2. Impact sur ControlHub AI
Explique ce que cette amélioration changerait concrètement dans le panel.

## 3. Fichiers probablement concernés
Liste les fichiers concernés et pourquoi.

## 4. Plan technique
Donne un plan en étapes.

## 5. Risques / points d'attention
Indique les risques techniques possibles.

## 6. Tests à faire
Liste les tests à effectuer dans l'interface.

## 7. Prochaine action recommandée
Dis exactement ce que Nolane devrait faire ensuite.
"""


def create_dev_task(request, request_type, analysis):
    tasks = load_json(TASKS_FILE, [])

    title = f"Dev ControlHub — {request_type}"

    description = f"""Demande :
{request}

Type :
{request_type}

Analyse Agent Développeur :
{analysis}
"""

    tasks.append(
        {
            "title": title,
            "category": "ControlHub AI",
            "priority": "haute",
            "status": "à faire",
            "linked_project": "ControlHub AI",
            "linked_agent": "Agent Développeur ControlHub",
            "due_date": "",
            "description": description,
        }
    )

    save_json(TASKS_FILE, tasks)

    add_action_log(
        source="Atelier Dev IA",
        action_type="Création tâche dev",
        title=title,
        details=description,
    )


def create_dev_mission(request, request_type, analysis):
    missions = load_json(AGENT_TASKS_FILE, [])

    title = f"Agent Développeur — {request_type}"

    context = f"""Demande :
{request}

Type :
{request_type}

Analyse :
{analysis}

Règles :
- Ne rien appliquer sans validation humaine.
- Expliquer les fichiers concernés.
- Préparer des fichiers complets si nécessaire.
- Journaliser les actions.
"""

    missions.append(
        {
            "agent": "Agent Développeur ControlHub",
            "title": title,
            "priority": "haute",
            "status": "à faire",
            "context": context,
        }
    )

    save_json(AGENT_TASKS_FILE, missions)

    add_action_log(
        source="Atelier Dev IA",
        action_type="Création mission dev",
        title=title,
        details=context,
    )


def save_dev_analysis_to_notes(request, request_type, analysis):
    note = f"""

## Analyse Agent Développeur — {request_type}

### Demande

{request}

### Analyse

{analysis}
"""

    with open(LEARNING_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(note)

    add_action_log(
        source="Atelier Dev IA",
        action_type="Création note dev",
        title=f"Analyse dev — {request_type}",
        details=note,
    )


def render_dev_workshop_page():
    profile, skills, projects, goals = load_all_data()

    st.title("🛠️ Atelier Dev IA")

    st.write(
        "Cette page permet à ControlHub AI de travailler sur son propre développement "
        "avec un Agent Développeur supervisé."
    )

    st.info(
        "Pour l’instant, l’agent analyse, propose, crée des tâches/missions/notes et journalise. "
        "Il ne modifie pas encore les fichiers automatiquement."
    )

    st.divider()

    request_type = st.selectbox(
        "Type de demande",
        [
            "Nouvelle fonctionnalité",
            "Correction bug",
            "Amélioration UI",
            "Refactor",
            "Agent IA",
            "Connecteur externe",
            "Automatisation",
            "Performance",
            "Sécurité / permissions",
            "Autre",
        ],
    )

    request = st.text_area(
        "Quelle amélioration veux-tu apporter à ControlHub AI ?",
        placeholder=(
            "Exemples :\n"
            "- Je veux que l’Atelier Dev IA puisse générer un fichier complet proposé.\n"
            "- Je veux améliorer le Pilotage central.\n"
            "- Je veux que les agents puissent préparer des commits.\n"
            "- Je veux ajouter une sauvegarde avant modification automatique."
        ),
        height=170,
    )

    external_context = st.text_area(
        "Informations externes fournies par toi, si nécessaire",
        placeholder=(
            "Colle ici une documentation, une erreur, une source web, un extrait de code, "
            "ou une précision que l’agent doit utiliser. L’agent ne cherche pas seul sur Internet."
        ),
        height=120,
    )

    available_models = get_ollama_models()
    selected_model = None

    if available_models:
        recommended_model = get_recommended_model(
            task_type="code",
            available_models=available_models,
        )

        model_options = ["Auto"] + available_models

        selected_model_choice = st.selectbox(
            "Modèle IA local",
            model_options,
            index=0,
        )

        if selected_model_choice == "Auto":
            selected_model = recommended_model
            st.info(f"Mode Auto : l’Atelier Dev IA utilisera probablement {recommended_model}.")
        else:
            selected_model = selected_model_choice

    response_style = st.selectbox(
        "Niveau de détail",
        [
            "Rapide",
            "Normal",
            "Détaillé",
        ],
        index=1,
    )

    st.divider()

    if st.button("Analyser avec l’Agent Développeur", key="dev-workshop-analyze"):
        if not request.strip():
            st.error("Décris d’abord l’amélioration souhaitée.")
            return

        prompt = build_dev_prompt(request, request_type, external_context)

        with st.spinner("Analyse de l’Agent Développeur en cours..."):
            analysis = generate_ai_response(
                prompt,
                profile,
                skills,
                projects,
                goals,
                model_name=selected_model,
                task_type="code",
                response_style=response_style,
            )

        st.session_state["dev_last_request"] = request
        st.session_state["dev_last_request_type"] = request_type
        st.session_state["dev_last_analysis"] = analysis

        add_action_log(
            source="Atelier Dev IA",
            action_type="Analyse dev IA",
            title=f"Analyse dev — {request_type}",
            details=f"Demande :\n{request}\n\nAnalyse :\n{analysis}",
        )

    if "dev_last_analysis" in st.session_state:
        st.divider()

        st.subheader("Analyse de l’Agent Développeur")
        st.markdown(st.session_state["dev_last_analysis"])

        st.divider()

        st.subheader("Actions depuis cette analyse")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Créer une tâche dev", key="dev-create-task"):
                create_dev_task(
                    st.session_state["dev_last_request"],
                    st.session_state["dev_last_request_type"],
                    st.session_state["dev_last_analysis"],
                )
                st.success("Tâche de développement créée.")

        with col2:
            if st.button("Créer une mission dev", key="dev-create-mission"):
                create_dev_mission(
                    st.session_state["dev_last_request"],
                    st.session_state["dev_last_request_type"],
                    st.session_state["dev_last_analysis"],
                )
                st.success("Mission Agent Développeur créée.")

        with col3:
            if st.button("Enregistrer dans Notes", key="dev-save-note"):
                save_dev_analysis_to_notes(
                    st.session_state["dev_last_request"],
                    st.session_state["dev_last_request_type"],
                    st.session_state["dev_last_analysis"],
                )
                st.success("Analyse enregistrée dans Notes.")

    st.divider()

    st.subheader("🧭 Évolution prévue")

    st.write(
        "Étape suivante : permettre à l’Agent Développeur de générer un fichier complet proposé "
        "dans un dossier `dev_proposals/`, sans modifier encore le vrai code."
    )