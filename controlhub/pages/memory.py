import streamlit as st

from controlhub.memory_tools import add_memory_item, load_memory
from controlhub.storage import MEMORY_FILE, save_json


def render_memory_page():
    st.title("🧠 Mémoire")

    st.write(
        "Cette page stocke les informations importantes que ControlHub AI doit retenir "
        "pour adapter ses réponses, ses agents et ses recommandations."
    )

    st.warning(
        "La mémoire reste locale. N’ajoute pas d’informations trop sensibles si tu prévois "
        "un jour de synchroniser ou déplacer tes fichiers."
    )

    memory = load_memory()

    with st.form("add_memory_form"):
        st.subheader("Ajouter une mémoire")

        category = st.selectbox(
            "Catégorie",
            [
                "Objectif long terme",
                "Préférence de travail",
                "Préférence d’apprentissage",
                "Carrière",
                "Projet",
                "Organisation personnelle",
                "Contrainte",
                "Décision importante",
                "Autre",
            ],
        )

        importance = st.selectbox(
            "Importance",
            [
                "basse",
                "moyenne",
                "haute",
            ],
            index=1,
        )

        content = st.text_area("Contenu à mémoriser")

        submitted = st.form_submit_button("Ajouter à la mémoire")

        if submitted:
            if content.strip():
                add_memory_item(category, content, importance)
                st.success("Mémoire ajoutée.")
                st.rerun()
            else:
                st.error("Le contenu est obligatoire.")

    st.divider()

    st.subheader("Mémoire enregistrée")

    if not memory:
        st.info("Aucune mémoire enregistrée pour le moment.")
        return

    high_memory = [item for item in memory if item.get("importance") == "haute"]
    medium_memory = [item for item in memory if item.get("importance") == "moyenne"]
    low_memory = [item for item in memory if item.get("importance") == "basse"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Haute importance", len(high_memory))

    with col2:
        st.metric("Importance moyenne", len(medium_memory))

    with col3:
        st.metric("Basse importance", len(low_memory))

    st.divider()

    for index, item in enumerate(memory, start=1):
        category = item.get("category", "Non catégorisé")
        importance = item.get("importance", "moyenne")
        content = item.get("content", "")

        with st.expander(f"{index}. {category} — {importance}"):
            st.write(content)

            if st.button("Supprimer cette mémoire", key=f"delete-memory-{index}"):
                memory.pop(index - 1)
                save_json(MEMORY_FILE, memory)
                st.success("Mémoire supprimée.")
                st.rerun()