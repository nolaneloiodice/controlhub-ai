import streamlit as st

from controlhub.action_log_tools import clear_action_log, load_action_log


def render_action_log_page():
    st.title("📜 Journal d’activité")

    st.write(
        "Cette page affiche l’historique des actions importantes réalisées dans ControlHub AI."
    )

    logs = load_action_log()

    if not logs:
        st.info("Aucune action enregistrée pour le moment.")
        return

    sources = sorted(set(log.get("source", "Inconnu") for log in logs))
    action_types = sorted(set(log.get("action_type", "Action") for log in logs))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Actions enregistrées", len(logs))

    with col2:
        st.metric("Sources", len(sources))

    with col3:
        st.metric("Types d’action", len(action_types))

    st.divider()

    selected_source = st.selectbox(
        "Filtrer par source",
        ["Toutes"] + sources,
    )

    selected_type = st.selectbox(
        "Filtrer par type",
        ["Tous"] + action_types,
    )

    filtered_logs = logs

    if selected_source != "Toutes":
        filtered_logs = [
            log for log in filtered_logs
            if log.get("source") == selected_source
        ]

    if selected_type != "Tous":
        filtered_logs = [
            log for log in filtered_logs
            if log.get("action_type") == selected_type
        ]

    st.subheader("Historique")

    for index, log in enumerate(filtered_logs, start=1):
        title = log.get("title", "Action sans titre")
        timestamp = log.get("timestamp", "Date inconnue")
        source = log.get("source", "Source inconnue")
        action_type = log.get("action_type", "Action")
        details = log.get("details", "")

        with st.expander(f"{index}. {title}"):
            st.write(f"**Date :** {timestamp}")
            st.write(f"**Source :** {source}")
            st.write(f"**Type :** {action_type}")

            if details:
                st.write("**Détails :**")
                st.write(details)

    st.divider()

    with st.expander("Zone dangereuse"):
        st.warning("Cette action vide le journal local.")
        if st.button("Vider le journal"):
            clear_action_log()
            st.success("Journal vidé.")
            st.rerun()