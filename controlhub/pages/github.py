import streamlit as st

from controlhub.github_tools import (
    generate_readme_template,
    generate_repository_suggestions,
    get_public_repositories,
)


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
            st.session_state["github_repositories"] = repositories
            st.success(f"{len(repositories)} repository(s) public(s) trouvé(s).")

        except Exception as error:
            st.error("Impossible de récupérer les repositories GitHub.")
            st.code(str(error))
            return

    repositories = st.session_state.get("github_repositories", [])

    if not repositories:
        st.info("Clique sur le bouton d’analyse pour charger tes repositories publics.")
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
        repo_name = repo.get("name", "repository")

        with st.expander(repo_name):
            st.write(
                f"**Description :** "
                f"{repo.get('description') or 'Aucune description'}"
            )
            st.write(f"**Langage :** {repo.get('language') or 'Non défini'}")
            st.write(f"**Étoiles :** {repo.get('stars')}")
            st.write(f"**Forks :** {repo.get('forks')}")
            st.write(f"**Dernière mise à jour :** {repo.get('updated_at')}")
            st.write(f"**Fork :** {'oui' if repo.get('is_fork') else 'non'}")
            st.write(f"**URL :** {repo.get('url')}")

            st.markdown("### Suggestions d’amélioration")

            suggestions = generate_repository_suggestions(repo)

            for index, suggestion in enumerate(suggestions):
                st.checkbox(
                    suggestion,
                    value=False,
                    key=f"{repo_name}-suggestion-{index}",
                )

            st.markdown("### Générateur README")

            if st.button(
                "Générer un modèle README",
                key=f"readme-button-{repo_name}",
            ):
                readme = generate_readme_template(repo)
                st.session_state[f"readme-template-{repo_name}"] = readme

            readme_key = f"readme-template-{repo_name}"

            if readme_key in st.session_state:
                st.text_area(
                    "Modèle README généré",
                    value=st.session_state[readme_key],
                    height=500,
                    key=f"readme-area-{repo_name}",
                )

                st.info(
                    "Tu peux copier ce README, l’adapter, puis le coller dans le repository concerné."
                )