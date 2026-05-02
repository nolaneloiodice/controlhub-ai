import streamlit as st

from controlhub.github_tools import get_public_repositories


DEFAULT_GITHUB_USERNAME = "nolaneloiodice"


def render_github_page():
    st.title("🐙 GitHub")

    st.write(
        "Cette page est le premier connecteur GitHub de ControlHub AI. "
        "Pour l’instant, elle fonctionne en lecture seule sur les repositories publics."
    )

    username = st.text_input(
        "Nom d'utilisateur GitHub",
        value=DEFAULT_GITHUB_USERNAME,
    )

    if st.button("Analyser mes repositories publics"):
        if not username.strip():
            st.error("Indique un nom d'utilisateur GitHub.")
            return

        try:
            repositories = get_public_repositories(username.strip())

            st.success(f"{len(repositories)} repository(s) public(s) trouvé(s).")

            if not repositories:
                st.write("Aucun repository public trouvé.")
                return

            languages = {}

            for repo in repositories:
                language = repo.get("language") or "Non défini"
                languages[language] = languages.get(language, 0) + 1

            st.subheader("Résumé")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Repositories publics", len(repositories))

            with col2:
                st.metric("Langages détectés", len(languages))

            st.write("**Répartition par langage :**")

            for language, count in languages.items():
                st.write(f"- {language} : {count}")

            st.divider()

            st.subheader("Repositories")

            for repo in repositories:
                with st.expander(repo.get("name", "Repository sans nom")):
                    st.write(f"**Description :** {repo.get('description') or 'Aucune description'}")
                    st.write(f"**Langage :** {repo.get('language') or 'Non défini'}")
                    st.write(f"**Étoiles :** {repo.get('stars')}")
                    st.write(f"**Forks :** {repo.get('forks')}")
                    st.write(f"**Dernière mise à jour :** {repo.get('updated_at')}")
                    st.write(f"**Fork :** {'oui' if repo.get('is_fork') else 'non'}")
                    st.write(f"**URL :** {repo.get('url')}")

                    st.markdown("### Suggestion locale")
                    st.write(
                        "Vérifie que ce repository possède un README clair avec : "
                        "objectif, contexte, technologies utilisées, étapes et compétences travaillées."
                    )

        except Exception as error:
            st.error("Impossible de récupérer les repositories GitHub.")
            st.code(str(error))