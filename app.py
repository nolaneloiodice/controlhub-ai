import json
from pathlib import Path

import streamlit as st


DATA_DIR = Path("data")
PROFILE_FILE = DATA_DIR / "profile.json"
SKILLS_FILE = DATA_DIR / "skills.json"
PROJECTS_FILE = DATA_DIR / "projects.json"
GOALS_FILE = DATA_DIR / "goals.json"


def load_json(file_path, default_data):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_data


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_all_data():
    profile = load_json(PROFILE_FILE, {})
    skills = load_json(SKILLS_FILE, [])
    projects = load_json(PROJECTS_FILE, [])
    goals = load_json(GOALS_FILE, [])
    return profile, skills, projects, goals


def page_home():
    profile, skills, projects, goals = load_all_data()

    st.title("🧠 ControlHub AI")
    st.write("Centre de contrôle personnel pour progresser en IT, réseaux, cybersécurité et IA.")

    name = profile.get("name", "Nolane")
    main_goal = profile.get("main_goal", "Construire un assistant personnel et progresser en IT/cyber.")

    st.subheader(f"Bienvenue, {name}")
    st.info(main_goal)

    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Compétences", len(skills))

    with col2:
        st.metric("Projets", len(projects))

    with col3:
        st.metric("Objectifs actifs", len(active_goals))

    st.divider()

    st.header("🔥 Priorité recommandée")

    high_priority_goals = [
        goal for goal in goals
        if goal.get("priority", "").lower() == "haute"
        and goal.get("status") != "terminé"
    ]

    if high_priority_goals:
        goal = high_priority_goals[0]
        st.success(goal.get("title", "Objectif prioritaire"))
        st.write(goal.get("description", ""))
    elif active_goals:
        goal = active_goals[0]
        st.info(goal.get("title", "Objectif à avancer"))
        st.write(goal.get("description", ""))
    else:
        st.warning("Aucun objectif actif. Ajoute un objectif pour guider ta progression.")

    st.divider()

    st.header("🧭 Prochaine logique de progression")
    st.write(
        "Pour ton profil BTS SIO SISR, la priorité est de consolider : "
        "**réseaux**, **Linux**, **cybersécurité défensive**, puis **Python/automatisation**."
    )


def page_skills():
    skills = load_json(SKILLS_FILE, [])

    st.title("🧩 Compétences")

    with st.form("add_skill_form"):
        st.subheader("Ajouter une compétence")

        name = st.text_input("Nom de la compétence")
        level = st.slider("Niveau", min_value=1, max_value=5, value=1)

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if name.strip():
                skills.append({
                    "name": name.strip(),
                    "level": level
                })
                save_json(SKILLS_FILE, skills)
                st.success("Compétence ajoutée.")
                st.rerun()
            else:
                st.error("Le nom de la compétence est obligatoire.")

    st.divider()

    st.subheader("Compétences suivies")

    if not skills:
        st.write("Aucune compétence enregistrée.")
    else:
        for skill in skills:
            skill_name = skill.get("name", "Compétence")
            level = skill.get("level", 1)

            st.write(f"**{skill_name}** — {level}/5")
            st.progress(level / 5)


def page_projects():
    projects = load_json(PROJECTS_FILE, [])

    st.title("🚀 Projets")

    with st.form("add_project_form"):
        st.subheader("Ajouter un projet")

        name = st.text_input("Nom du projet")
        category = st.text_input("Catégorie", placeholder="Réseaux, Systèmes, Cyber, Python, IA...")
        status = st.selectbox("Statut", ["idée", "en cours", "terminé", "en pause"])
        github_url = st.text_input("Lien GitHub")
        description = st.text_area("Description courte")
        skills_input = st.text_input("Compétences liées, séparées par des virgules")

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if name.strip():
                skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]

                projects.append({
                    "name": name.strip(),
                    "category": category.strip(),
                    "status": status,
                    "github_url": github_url.strip(),
                    "description": description.strip(),
                    "skills": skills
                })

                save_json(PROJECTS_FILE, projects)
                st.success("Projet ajouté.")
                st.rerun()
            else:
                st.error("Le nom du projet est obligatoire.")

    st.divider()

    st.subheader("Projets enregistrés")

    if not projects:
        st.write("Aucun projet enregistré.")
    else:
        for project in projects:
            with st.expander(project.get("name", "Projet sans nom")):
                st.write(f"**Catégorie :** {project.get('category', 'Non définie')}")
                st.write(f"**Statut :** {project.get('status', 'Non défini')}")
                st.write(f"**GitHub :** {project.get('github_url', '')}")
                st.write(project.get("description", ""))

                skills = project.get("skills", [])
                if skills:
                    st.write("**Compétences liées :**")
                    st.write(", ".join(skills))


def page_goals():
    goals = load_json(GOALS_FILE, [])

    st.title("🎯 Objectifs")

    with st.form("add_goal_form"):
        st.subheader("Ajouter un objectif")

        title = st.text_input("Titre de l'objectif")
        category = st.text_input("Catégorie", placeholder="Systèmes, Réseaux, Cyber, Python, Portfolio...")
        priority = st.selectbox("Priorité", ["basse", "moyenne", "haute"])
        status = st.selectbox("Statut", ["en cours", "terminé", "en pause"])
        description = st.text_area("Description courte")

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if title.strip():
                goals.append({
                    "title": title.strip(),
                    "category": category.strip(),
                    "priority": priority,
                    "status": status,
                    "description": description.strip()
                })

                save_json(GOALS_FILE, goals)
                st.success("Objectif ajouté.")
                st.rerun()
            else:
                st.error("Le titre de l'objectif est obligatoire.")

    st.divider()

    st.subheader("Objectifs enregistrés")

    if not goals:
        st.write("Aucun objectif enregistré.")
    else:
        for goal in goals:
            with st.expander(goal.get("title", "Objectif sans titre")):
                st.write(f"**Catégorie :** {goal.get('category', 'Non définie')}")
                st.write(f"**Priorité :** {goal.get('priority', 'Non définie')}")
                st.write(f"**Statut :** {goal.get('status', 'Non défini')}")
                st.write(goal.get("description", ""))


def page_roadmap():
    st.title("🧭 Roadmap")

    st.write(
        "Cette roadmap sert à structurer ta progression vers le BTS SIO SISR, "
        "les systèmes, réseaux, cybersécurité et l’automatisation avec Python/IA."
    )

    roadmap = [
        {
            "phase": "Phase 1 — Fondations",
            "status": "en cours",
            "tasks": [
                "Consolider Git/GitHub",
                "Continuer ControlHub AI",
                "Documenter les apprentissages dans le learning log",
                "Organiser les projets existants"
            ]
        },
        {
            "phase": "Phase 2 — Réseaux",
            "status": "en cours",
            "tasks": [
                "Améliorer les README des labs Cisco Packet Tracer",
                "Revoir IP, masque, passerelle, DNS, DHCP",
                "Revoir VLAN, routage inter-VLAN et NAT/PAT",
                "Ajouter un lab ACL si nécessaire"
            ]
        },
        {
            "phase": "Phase 3 — Linux / Systèmes",
            "status": "à reprendre",
            "tasks": [
                "Reprendre la VM Ubuntu",
                "Diagnostiquer Apache",
                "Comprendre systemctl, services, ports et pare-feu",
                "Créer un mini-projet GitHub Ubuntu Web Server Lab"
            ]
        },
        {
            "phase": "Phase 4 — Cybersécurité défensive",
            "status": "commencé",
            "tasks": [
                "Continuer TryHackMe",
                "Résumer chaque room importante",
                "Comprendre logs, détection, durcissement et bonnes pratiques",
                "Créer des notes cyber en français"
            ]
        },
        {
            "phase": "Phase 5 — Portfolio professionnel",
            "status": "en cours",
            "tasks": [
                "Rendre GitHub plus lisible",
                "Ajouter des descriptions propres aux projets",
                "Préparer des posts LinkedIn",
                "Préparer le pitch alternance BTS SIO SISR"
            ]
        },
        {
            "phase": "Phase 6 — IA / Automatisation",
            "status": "en construction",
            "tasks": [
                "Améliorer le dashboard ControlHub AI",
                "Ajouter une vraie génération de tâches",
                "Ajouter une page notes",
                "Connecter une IA plus tard"
            ]
        }
    ]

    for item in roadmap:
        with st.expander(f"{item['phase']} — {item['status']}"):
            for task in item["tasks"]:
                st.checkbox(task, value=False)

    st.divider()

    st.header("🔥 Prochaine action recommandée")

    st.success("Reprendre le lab Ubuntu Apache")
    st.write(
        "C’est une bonne priorité car elle relie Linux, réseau, services système, "
        "diagnostic et cybersécurité de base."
    )

    st.markdown("### Plan rapide")
    st.write("1. Démarrer la VM Ubuntu")
    st.write("2. Vérifier si Apache est installé")
    st.write("3. Vérifier le statut du service Apache")
    st.write("4. Vérifier le port 80")
    st.write("5. Tester dans le navigateur")
    st.write("6. Noter le résultat dans le learning log")


def page_ai_assistant():
    st.title("🤖 Assistant IA")

    st.info("Cette page préparera l’intégration IA. Pour l’instant, elle sert de prototype d’interface.")

    prompt = st.text_area(
        "Demande à ton futur assistant :",
        placeholder="Exemple : Génère-moi une tâche du jour pour progresser en Linux et cybersécurité."
    )

    if st.button("Générer une réponse prototype"):
        if prompt.strip():
            st.subheader("Réponse prototype")
            st.write(
                "Pour l’instant, l’IA n’est pas encore connectée. "
                "Mais cette zone servira bientôt à générer des tâches, résumés, posts LinkedIn, README et plans d’apprentissage."
            )

            st.markdown("### Exemple de tâche")
            st.write(
                "Travaille 45 minutes sur ton objectif prioritaire, puis ajoute un résumé dans ton learning log."
            )
        else:
            st.warning("Écris d’abord une demande.")


def main():
    st.set_page_config(
        page_title="ControlHub AI",
        page_icon="🧠",
        layout="wide"
    )

    st.sidebar.title("🧠 ControlHub AI")
    st.sidebar.write("Bureau de contrôle personnel")

    page = st.sidebar.radio(
    "Navigation",
    [
        "Accueil",
        "Compétences",
        "Projets",
        "Objectifs",
        "Roadmap",
        "Assistant IA"
    ]
)

    st.sidebar.divider()
    st.sidebar.caption("Version 0.2 — Dashboard local")

    if page == "Accueil":
        page_home()
    elif page == "Compétences":
        page_skills()
    elif page == "Projets":
        page_projects()
    elif page == "Objectifs":
        page_goals()
    elif page == "Roadmap":
        page_roadmap()
    elif page == "Assistant IA":
        page_ai_assistant()


if __name__ == "__main__":
    main()