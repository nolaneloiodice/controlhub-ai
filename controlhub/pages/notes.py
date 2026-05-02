import streamlit as st

from controlhub.storage import LEARNING_LOG_FILE


def render_notes_page():
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
                "Autre",
            ],
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