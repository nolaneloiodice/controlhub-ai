import streamlit as st

from controlhub.agents import get_priority_goal, run_agent_action
from controlhub.storage import load_all_data


def render_ai_assistant_page():
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
            "Action pour l’objectif prioritaire",
        ],
    )

    priority_goal = get_priority_goal(goals)

    if st.button("Générer"):
        if action == "Tâche du jour":
            st.subheader("✅ Tâche du jour")
            result = run_agent_action("Générer une tâche prioritaire", profile, skills, projects, goals)
            st.markdown(result)

        elif action == "Résumé de progression":
            st.subheader("📈 Résumé de progression")
            result = run_agent_action("Résumer ma progression", profile, skills, projects, goals)
            st.markdown(result)

        elif action == "Idée de post LinkedIn":
            st.subheader("💼 Idée de post LinkedIn")
            result = run_agent_action("Préparer un post LinkedIn", profile, skills, projects, goals)
            st.markdown(result)
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
                    language="markdown",
                )
            else:
                st.warning("Aucun objectif actif trouvé. Ajoute un objectif dans l’onglet Objectifs.")