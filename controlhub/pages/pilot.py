import streamlit as st


def go_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()


def analyze_request(user_request):
    request = user_request.lower().strip()

    suggestions = []

    def add(page, title, reason, priority=1):
        suggestions.append(
            {
                "page": page,
                "title": title,
                "reason": reason,
                "priority": priority,
            }
        )

    if not request:
        return []

    if any(word in request for word in ["aujourd", "maintenant", "priorité", "quoi faire", "journée", "optimisé"]):
        add(
            "Aujourd'hui",
            "Voir quoi faire maintenant",
            "Ta demande concerne la priorité immédiate ou l’organisation de ta journée.",
            10,
        )

    if any(word in request for word in ["tâche", "task", "planning", "todo", "à faire", "planifier"]):
        add(
            "Tâches / Planning",
            "Gérer tes tâches",
            "Ta demande concerne une action concrète à suivre.",
            9,
        )

    if any(word in request for word in ["mission", "agent", "agents", "exécuter", "plan d’exécution"]):
        add(
            "Missions Agents",
            "Piloter les missions agents",
            "Ta demande concerne les missions confiées aux agents IA.",
            9,
        )

    if any(word in request for word in ["github", "repo", "repository", "readme", "portfolio", "public"]):
        if any(word in request for word in ["créer", "nouveau", "publier", "préparer", "builder"]):
            add(
                "Repo Builder",
                "Préparer un repository GitHub",
                "Ta demande concerne la création ou préparation d’un repo à partir d’un projet.",
                10,
            )
        else:
            add(
                "GitHub",
                "Analyser tes repositories GitHub",
                "Ta demande concerne tes repositories existants, README ou portfolio GitHub.",
                8,
            )

    if any(word in request for word in ["projet", "projects"]):
        add(
            "Projets",
            "Gérer tes projets",
            "Ta demande concerne un projet enregistré dans ControlHub AI.",
            7,
        )

    if any(word in request for word in ["objectif", "objectifs", "but", "priorité long terme"]):
        add(
            "Objectifs",
            "Gérer tes objectifs",
            "Ta demande concerne tes objectifs ou priorités.",
            7,
        )

    if any(word in request for word in ["note", "notes", "résumé", "résumer", "learning log", "mémoriser"]):
        add(
            "Notes",
            "Écrire ou consulter tes notes",
            "Ta demande concerne la mémorisation, les résumés ou le learning log.",
            8,
        )

    if any(word in request for word in ["session", "travailler", "apprendre", "réviser", "lab", "tryhackme"]):
        add(
            "Session du jour",
            "Lancer une session structurée",
            "Ta demande concerne une session de travail ou d’apprentissage.",
            8,
        )

    if any(word in request for word in ["ia", "assistant", "rédige", "écris", "décision", "choix", "optimisé", "aide-moi"]):
        add(
            "Assistant IA",
            "Demander à l’assistant IA",
            "Ta demande nécessite une génération, une analyse ou une aide personnalisée.",
            9,
        )

    if any(word in request for word in ["souviens", "mémoire", "préférence", "retenir", "adapte-toi"]):
        add(
            "Mémoire",
            "Ajouter ou consulter la mémoire",
            "Ta demande concerne ce que ControlHub AI doit retenir sur toi.",
            9,
        )

    if any(word in request for word in ["compétence", "niveau", "skills", "progression"]):
        add(
            "Compétences",
            "Suivre tes compétences",
            "Ta demande concerne tes compétences ou ton niveau.",
            6,
        )

    if any(word in request for word in ["roadmap", "parcours", "chemin", "plan long terme"]):
        add(
            "Roadmap",
            "Voir ta roadmap",
            "Ta demande concerne ta direction globale ou ton plan long terme.",
            6,
        )

    if any(word in request for word in ["linkedin", "email", "mail", "entretien", "alternance", "cv", "carrière"]):
        add(
            "Assistant IA",
            "Préparer un contenu carrière",
            "Ta demande concerne LinkedIn, email, entretien, alternance ou carrière.",
            10,
        )

        add(
            "Missions Agents",
            "Créer une mission carrière",
            "Tu peux transformer cette demande en mission pour l’Agent Carrière.",
            7,
        )

    if not suggestions:
        add(
            "Assistant IA",
            "Analyser ta demande avec l’IA",
            "Je n’ai pas identifié une page précise. L’assistant IA peut analyser ta demande.",
            5,
        )

    suggestions = sorted(
        suggestions,
        key=lambda item: item["priority"],
        reverse=True,
    )

    unique_suggestions = []
    seen_pages = set()

    for suggestion in suggestions:
        if suggestion["page"] not in seen_pages:
            unique_suggestions.append(suggestion)
            seen_pages.add(suggestion["page"])

    return unique_suggestions[:4]


def render_quick_actions():
    st.subheader("⚡ Actions rapides")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Quoi faire maintenant ?"):
            go_to_page("Aujourd'hui")

        if st.button("Créer une tâche"):
            go_to_page("Tâches / Planning")

    with col2:
        if st.button("Piloter mes agents"):
            go_to_page("Missions Agents")

        if st.button("Créer un repo"):
            go_to_page("Repo Builder")

    with col3:
        if st.button("Demander à l’IA"):
            go_to_page("Assistant IA")

        if st.button("Écrire une note"):
            go_to_page("Notes")

    with col4:
        if st.button("Analyser GitHub"):
            go_to_page("GitHub")

        if st.button("Ajouter mémoire"):
            go_to_page("Mémoire")


def render_pilot_page():
    st.title("🎛️ Pilotage central")

    st.write(
        "Décris ce que tu veux faire, et ControlHub AI t’envoie vers le bon module."
    )

    st.info(
        "Cette page devient ton point central : au lieu de chercher dans tous les onglets, "
        "tu écris ton besoin et le panel te guide."
    )

    st.divider()

    user_request = st.text_area(
        "Que veux-tu faire ?",
        placeholder=(
            "Exemples :\n"
            "- Je veux créer un repo pour mon projet Ubuntu\n"
            "- Je ne sais pas quoi faire aujourd’hui\n"
            "- Je veux préparer un post LinkedIn\n"
            "- Je veux transformer une mission en tâche\n"
            "- Je veux noter ce que j’ai appris"
        ),
        height=150,
    )

    if st.button("Trouver le bon module"):
        suggestions = analyze_request(user_request)

        st.session_state["pilot_suggestions"] = suggestions
        st.session_state["pilot_last_request"] = user_request

    if "pilot_suggestions" in st.session_state:
        st.subheader("🎯 Modules recommandés")

        suggestions = st.session_state["pilot_suggestions"]

        if not suggestions:
            st.warning("Je n’ai pas trouvé de module adapté.")
        else:
            for index, suggestion in enumerate(suggestions, start=1):
                with st.container():
                    st.markdown(f"### {index}. {suggestion['title']}")
                    st.write(f"**Module :** {suggestion['page']}")
                    st.write(suggestion["reason"])

                    if st.button(
                        f"Aller vers {suggestion['page']}",
                        key=f"go-to-{suggestion['page']}-{index}",
                    ):
                        go_to_page(suggestion["page"])

                    st.divider()

    render_quick_actions()

    st.divider()

    st.subheader("🧠 Conseil")

    st.write(
        "À terme, cette page pourra devenir un vrai routeur intelligent : "
        "elle pourra créer directement une tâche, une mission agent, une note ou un plan IA selon ta demande."
    )