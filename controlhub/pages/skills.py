import streamlit as st

from controlhub.storage import SKILLS_FILE, load_json, save_json


def render_skills_page():
    skills = load_json(SKILLS_FILE, [])

    st.title("🧩 Compétences")

    with st.form("add_skill_form"):
        st.subheader("Ajouter une compétence")

        name = st.text_input("Nom de la compétence")
        level = st.slider("Niveau", min_value=1, max_value=5, value=1)

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if name.strip():
                skills.append(
                    {
                        "name": name.strip(),
                        "level": level,
                    }
                )

                save_json(SKILLS_FILE, skills)
                st.success("Compétence ajoutée.")
                st.rerun()
            else:
                st.error("Le nom de la compétence est obligatoire.")

    st.divider()

    st.subheader("Compétences suivies")

    if not skills:
        st.write("Aucune compétence enregistrée.")
        return

    average_level = sum(skill.get("level", 1) for skill in skills) / len(skills)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Nombre de compétences", len(skills))

    with col2:
        st.metric("Niveau moyen", f"{average_level:.1f}/5")

    for skill in skills:
        skill_name = skill.get("name", "Compétence")
        level = skill.get("level", 1)

        st.write(f"**{skill_name}** — {level}/5")
        st.progress(level / 5)