import streamlit as st

from controlhub.storage import GOALS_FILE, load_json, save_json


def render_goals_page():
    goals = load_json(GOALS_FILE, [])

    st.title("🎯 Objectifs")

    with st.form("add_goal_form"):
        st.subheader("Ajouter un objectif")

        title = st.text_input("Titre de l'objectif")
        category = st.text_input(
            "Catégorie",
            placeholder="Systèmes, Réseaux, Cyber, Python, Portfolio...",
        )
        priority = st.selectbox("Priorité", ["basse", "moyenne", "haute"])
        status = st.selectbox("Statut", ["en cours", "terminé", "en pause"])
        description = st.text_area("Description courte")

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if title.strip():
                goals.append(
                    {
                        "title": title.strip(),
                        "category": category.strip(),
                        "priority": priority,
                        "status": status,
                        "description": description.strip(),
                    }
                )

                save_json(GOALS_FILE, goals)
                st.success("Objectif ajouté.")
                st.rerun()
            else:
                st.error("Le titre de l'objectif est obligatoire.")

    st.divider()

    st.subheader("Objectifs enregistrés")

    if not goals:
        st.write("Aucun objectif enregistré.")
        return

    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]
    done_goals = [goal for goal in goals if goal.get("status") == "terminé"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Objectifs actifs", len(active_goals))

    with col2:
        st.metric("Objectifs terminés", len(done_goals))

    for index, goal in enumerate(goals, start=1):
        with st.expander(f"{index}. {goal.get('title', 'Objectif sans titre')}"):
            st.write(f"**Catégorie :** {goal.get('category', 'Non définie')}")
            st.write(f"**Priorité :** {goal.get('priority', 'Non définie')}")
            st.write(f"**Statut :** {goal.get('status', 'Non défini')}")
            st.write(goal.get("description", ""))