import streamlit as st

from controlhub.ai_tools import (
    generate_ai_response,
    get_ai_provider,
    get_ai_status,
    get_ollama_model,
    get_ollama_models,
)
from controlhub.agents import get_priority_goal, run_agent_action
from controlhub.storage import load_all_data


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

    selected_model = None

    if provider == "ollama":
        available_models = get_ollama_models()

        if available_models:
            default_model = get_ollama_model()

            if default_model in available_models:
                default_index = available_models.index(default_model)
            else:
                default_index = 0

            selected_model = st.selectbox(
                "Modèle IA local",
                available_models,
                index=default_index,
            )

            if "coder" in selected_model.lower():
                st.info("Modèle orienté code / technique sélectionné.")
            elif "llama" in selected_model.lower():
                st.info("Modèle général sélectionné.")
            else:
                st.info("Modèle local sélectionné.")
        else:
            st.warning("Aucun modèle Ollama détecté. Vérifie `ollama list`.")

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

    default_prompt = ""

    if mode == "Tâche du jour":
        default_prompt = (
            "Analyse mes objectifs, projets et compétences. "
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
            )

        st.subheader("Réponse IA")
        st.markdown(result)

    if fallback_button:
        st.subheader("Réponse locale")

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

        st.markdown(result)