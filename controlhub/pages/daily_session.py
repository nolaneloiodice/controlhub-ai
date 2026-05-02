import streamlit as st

from controlhub.storage import LEARNING_LOG_FILE, load_all_data


def render_daily_session_page():
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
            selected_goal = st.text_input(
                "Objectif travaillé",
                placeholder="Exemple : Reprendre le lab Ubuntu Apache",
            )

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
                "Autre",
            ],
        )

        duration = st.selectbox(
            "Durée prévue",
            [
                "30 minutes",
                "45 minutes",
                "1 heure",
                "1h30",
                "2 heures",
                "3 heures",
            ],
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