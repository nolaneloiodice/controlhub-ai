import streamlit as st

from controlhub.ai_tools import (
    generate_ai_response,
    get_ai_provider,
    get_ai_status,
    get_ollama_models,
    get_recommended_model,
)
from controlhub.agents import get_priority_goal, run_agent_action
from controlhub.storage import (
    AGENT_TASKS_FILE,
    LEARNING_LOG_FILE,
    TASKS_FILE,
    load_all_data,
    load_json,
    save_json,
)


def get_task_type_from_mode(mode):
    if mode == "Code / Debug Python":
        return "code"

    if mode == "Préparation GitHub":
        return "github"

    if mode == "Idée de post LinkedIn":
        return "writing"

    if mode == "Préparation entretien":
        return "career"

    if mode == "Organisation de vie":
        return "planning"

    if mode == "Décision optimisée":
        return "decision"

    return "general"


def save_ai_response_to_notes(mode, prompt, response):
    note = f"""

## Réponse IA — {mode}

### Demande

{prompt}

### Réponse

{response}
"""

    with open(LEARNING_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(note)


def create_task_from_ai_response(mode, prompt, response):
    tasks = load_json(TASKS_FILE, [])

    tasks.append(
        {
            "title": f"Action IA — {mode}",
            "category": "ControlHub AI",
            "priority": "moyenne",
            "status": "à faire",
            "linked_project": "",
            "linked_agent": "Assistant IA",
            "due_date": "",
            "description": f"Demande :\n{prompt}\n\nRéponse IA :\n{response}",
        }
    )

    save_json(TASKS_FILE, tasks)


def create_mission_from_ai_response(mode, prompt, response):
    missions = load_json(AGENT_TASKS_FILE, [])

    missions.append(
        {
            "agent": "Agent Automatisation",
            "title": f"Traiter réponse IA — {mode}",
            "priority": "moyenne",
            "status": "à faire",
            "context": f"Demande :\n{prompt}\n\nRéponse IA :\n{response}",
        }
    )

    save_json(AGENT_TASKS_FILE, missions)


def render_ai_assistant_page():
    profile, skills, projects, goals = load_all_data()

    st.title("🤖 Assistant IA")

    provider = get_ai_provider()
    status = get_ai_status()

    if provider == "ollama" and "connectée" in status:
        st.success(status)
    elif provider == "openai" and "connectée" in status:
        st.success(status)
    else:
        st.warning(status)

    st.write(
        "Cette page permet de demander à l’assistant IA d’analyser tes données locales "
        "et de générer des réponses personnalisées."
    )

    st.caption(
        "Mode recommandé actuellement : Ollama local. Tes données restent sur ton PC."
    )

    st.divider()

    mode = st.selectbox(
        "Mode",
        [
            "Demande libre",
            "Tâche du jour",
            "Résumé de progression",
            "Idée de post LinkedIn",
            "Action pour l’objectif prioritaire",
            "Préparation GitHub",
            "Préparation entretien",
            "Décision optimisée",
            "Organisation de vie",
            "Code / Debug Python",
        ],
    )

    task_type = get_task_type_from_mode(mode)
    selected_model = None

    if provider == "ollama":
        available_models = get_ollama_models()

        if available_models:
            model_options = ["Auto"] + available_models

            selected_model_choice = st.selectbox(
                "Modèle IA local",
                model_options,
                index=0,
            )

            recommended_model = get_recommended_model(
                task_type=task_type,
                available_models=available_models,
            )

            if selected_model_choice == "Auto":
                selected_model = None
                st.info(f"Mode Auto : ControlHub utilisera probablement {recommended_model}.")
            else:
                selected_model = selected_model_choice

                if "coder" in selected_model.lower():
                    st.info("Modèle orienté code / technique sélectionné.")
                elif "llama" in selected_model.lower():
                    st.info("Modèle général sélectionné.")
                else:
                    st.info("Modèle local sélectionné.")
        else:
            st.warning("Aucun modèle Ollama détecté. Vérifie ollama list.")

    response_style = st.selectbox(
        "Style de réponse",
        [
            "Rapide",
            "Normal",
            "Détaillé",
        ],
        index=1,
    )

    st.caption(
        "Rapide = plus court et plus fluide. Détaillé = plus complet mais plus lent."
    )

    st.divider()

    default_prompt = ""

    if mode == "Tâche du jour":
        default_prompt = (
            "Analyse mes objectifs, projets, tâches et compétences. "
            "Génère une tâche du jour claire, réaliste, avec une durée conseillée et un plan d’action."
        )

    elif mode == "Résumé de progression":
        default_prompt = (
            "Fais un résumé professionnel de ma progression actuelle, "
            "en mettant en avant mes compétences, projets et objectifs."
        )

    elif mode == "Idée de post LinkedIn":
        default_prompt = (
            "Prépare un post LinkedIn professionnel sur ma progression avec ControlHub AI, "
            "mon parcours BTS SIO SISR, GitHub, réseaux, Linux et cybersécurité."
        )

    elif mode == "Action pour l’objectif prioritaire":
        priority_goal = get_priority_goal(goals)

        if priority_goal:
            default_prompt = (
                f"Prépare un plan d’action concret pour mon objectif prioritaire : "
                f"{priority_goal.get('title')}. "
                f"Description : {priority_goal.get('description', '')}"
            )
        else:
            default_prompt = "Aide-moi à définir un objectif prioritaire utile."

    elif mode == "Préparation GitHub":
        default_prompt = (
            "Analyse mes projets et propose les meilleures actions pour améliorer mon GitHub "
            "et le rendre plus professionnel pour une alternance BTS SIO SISR."
        )

    elif mode == "Préparation entretien":
        default_prompt = (
            "Prépare-moi un pitch d’entretien pour une alternance BTS SIO SISR, "
            "en valorisant mon parcours, mes labs GitHub, ControlHub AI, Linux, réseaux et cybersécurité."
        )

    elif mode == "Décision optimisée":
        default_prompt = (
            "Aide-moi à prendre une décision optimisée. "
            "Pose le problème, compare les options, liste avantages/inconvénients, "
            "puis recommande l’action la plus utile."
        )

    elif mode == "Organisation de vie":
        default_prompt = (
            "Aide-moi à organiser ma journée ou ma semaine en tenant compte de mes projets, "
            "objectifs, apprentissages, énergie et priorités."
        )

    elif mode == "Code / Debug Python":
        default_prompt = (
            "Aide-moi à comprendre ou corriger mon code Python. "
            "Explique simplement le problème, propose une correction propre, "
            "et indique ce que je dois retenir."
        )

    prompt = st.text_area(
        "Demande à l’assistant",
        value=default_prompt,
        height=180,
    )

    col1, col2 = st.columns(2)

    with col1:
        generate_button = st.button("Générer avec l’IA locale")

    with col2:
        fallback_button = st.button("Générer avec le moteur local")

    if generate_button:
        if not prompt.strip():
            st.error("Écris une demande avant de générer.")
            return

        with st.spinner("Génération en cours avec l’IA locale..."):
            result = generate_ai_response(
                prompt,
                profile,
                skills,
                projects,
                goals,
                model_name=selected_model,
                task_type=task_type,
                response_style=response_style,
            )

        st.session_state["last_ai_mode"] = mode
        st.session_state["last_ai_prompt"] = prompt
        st.session_state["last_ai_response"] = result

    if fallback_button:
        if mode == "Tâche du jour":
            result = run_agent_action(
                "Générer une tâche prioritaire",
                profile,
                skills,
                projects,
                goals,
            )
        elif mode == "Résumé de progression":
            result = run_agent_action(
                "Résumer ma progression",
                profile,
                skills,
                projects,
                goals,
            )
        elif mode == "Idée de post LinkedIn":
            result = run_agent_action(
                "Préparer un post LinkedIn",
                profile,
                skills,
                projects,
                goals,
            )
        elif mode == "Préparation GitHub":
            result = run_agent_action(
                "Proposer une amélioration GitHub",
                profile,
                skills,
                projects,
                goals,
            )
        else:
            result = (
                "Le moteur local est limité pour ce mode. "
                "Utilise la génération IA locale pour une réponse plus personnalisée."
            )

        st.session_state["last_ai_mode"] = mode
        st.session_state["last_ai_prompt"] = prompt
        st.session_state["last_ai_response"] = result

    if "last_ai_response" in st.session_state:
        st.divider()

        st.subheader("Réponse IA")
        st.markdown(st.session_state["last_ai_response"])

        st.divider()

        st.subheader("Actions sur cette réponse")

        action_col1, action_col2, action_col3 = st.columns(3)

        with action_col1:
            if st.button("Enregistrer dans Notes"):
                save_ai_response_to_notes(
                    st.session_state["last_ai_mode"],
                    st.session_state["last_ai_prompt"],
                    st.session_state["last_ai_response"],
                )
                st.success("Réponse enregistrée dans Notes.")

        with action_col2:
            if st.button("Créer une tâche"):
                create_task_from_ai_response(
                    st.session_state["last_ai_mode"],
                    st.session_state["last_ai_prompt"],
                    st.session_state["last_ai_response"],
                )
                st.success("Tâche créée dans Tâches / Planning.")

        with action_col3:
            if st.button("Créer une mission agent"):
                create_mission_from_ai_response(
                    st.session_state["last_ai_mode"],
                    st.session_state["last_ai_prompt"],
                    st.session_state["last_ai_response"],
                )
                st.success("Mission créée dans Missions Agents.")