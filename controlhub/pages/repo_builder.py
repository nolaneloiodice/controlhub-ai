import streamlit as st

from controlhub.storage import (
    AGENT_TASKS_FILE,
    PROJECTS_FILE,
    load_json,
    save_json,
)


def slugify_project_name(name):
    slug = name.lower()
    replacements = {
        " ": "-",
        "_": "-",
        "/": "-",
        "\\": "-",
        ":": "",
        "'": "",
        "’": "",
        ",": "",
        ".": "",
        "(": "",
        ")": "",
    }

    for old, new in replacements.items():
        slug = slug.replace(old, new)

    while "--" in slug:
        slug = slug.replace("--", "-")

    return slug.strip("-")


def generate_repo_description(project):
    name = project.get("name", "Projet")
    category = project.get("category", "IT")
    description = project.get("description", "")

    if description:
        return description[:160]

    return f"Projet {category} : {name}"


def generate_project_readme(project):
    name = project.get("name", "Projet sans nom")
    category = project.get("category", "Non définie")
    status = project.get("status", "Non défini")
    description = project.get("description", "Description à compléter.")
    skills = project.get("skills", [])

    skills_section = "\n".join([f"- {skill}" for skill in skills]) or "- À compléter"

    return f"""# {name}

## Présentation

{description}

## Catégorie

{category}

## Statut

{status}

## Objectif du projet

Décrire ici l’objectif principal du projet.

## Compétences travaillées

{skills_section}

## Technologies / outils utilisés

- À compléter
- À compléter
- À compléter

## Étapes principales

1. Préparation du projet
2. Mise en place de l’environnement
3. Réalisation des tests
4. Documentation
5. Publication sur GitHub

## Résultat attendu

Décrire ici le résultat attendu ou obtenu.

## Difficultés rencontrées

- À compléter

## Améliorations futures

- Améliorer la documentation
- Ajouter des captures ou schémas
- Ajouter des exemples
- Ajouter une conclusion technique
"""


def generate_file_structure(project):
    category = project.get("category", "").lower()

    if "réseau" in category or "network" in category or "cisco" in category:
        return """repo/
├── README.md
├── topology/
│   └── topology.png
├── packet-tracer/
│   └── lab.pkt
└── docs/
    └── notes.md
"""

    if "python" in category or "ia" in category or "ai" in category:
        return """repo/
├── README.md
├── main.py
├── requirements.txt
├── docs/
│   └── notes.md
└── tests/
"""

    if "système" in category or "linux" in category:
        return """repo/
├── README.md
├── commands.md
├── screenshots/
└── docs/
    └── troubleshooting.md
"""

    return """repo/
├── README.md
├── docs/
│   └── notes.md
└── assets/
"""


def create_repo_builder_mission(project, repo_name, repo_description, structure, readme):
    tasks = load_json(AGENT_TASKS_FILE, [])

    project_name = project.get("name", "Projet sans nom")
    project_category = project.get("category", "Non définie")
    project_status = project.get("status", "Non défini")

    context = f"""Projet source : {project_name}
Catégorie : {project_category}
Statut : {project_status}

Objectif :
Préparer la création d’un repository GitHub à partir de ce projet ControlHub AI.

Nom recommandé du repository :
{repo_name}

Description GitHub recommandée :
{repo_description}

Structure recommandée :
{structure}

README proposé :
{readme}

Consignes :
- Ne rien créer automatiquement sans validation humaine.
- Vérifier qu’aucune donnée personnelle sensible n’est présente.
- Adapter le README avant publication si nécessaire.
- Préparer ensuite la création du repository GitHub.
"""

    tasks.append(
        {
            "agent": "Agent GitHub",
            "title": f"Créer/préparer repository GitHub pour {project_name}",
            "priority": "haute",
            "status": "à faire",
            "context": context,
        }
    )

    save_json(AGENT_TASKS_FILE, tasks)


def render_repo_builder_page():
    st.title("🏗️ Repo Builder")

    st.write(
        "Cette page prépare la création d’un repository GitHub à partir d’un projet enregistré. "
        "Pour l’instant, rien n’est créé automatiquement : ControlHub AI génère seulement un plan prêt à valider."
    )

    projects = load_json(PROJECTS_FILE, [])

    if not projects:
        st.warning("Aucun projet enregistré. Ajoute d’abord un projet dans l’onglet Projets.")
        return

    project_names = [project.get("name", "Projet sans nom") for project in projects]

    selected_project_name = st.selectbox(
        "Choisir un projet",
        project_names,
    )

    selected_project = None

    for project in projects:
        if project.get("name", "Projet sans nom") == selected_project_name:
            selected_project = project
            break

    if not selected_project:
        st.error("Projet introuvable.")
        return

    st.divider()

    st.subheader("Résumé du projet")

    st.write(f"**Nom :** {selected_project.get('name')}")
    st.write(f"**Catégorie :** {selected_project.get('category')}")
    st.write(f"**Statut :** {selected_project.get('status')}")
    st.write(f"**Description :** {selected_project.get('description')}")

    st.divider()

    repo_name = slugify_project_name(selected_project.get("name", "projet"))
    repo_description = generate_repo_description(selected_project)
    readme = generate_project_readme(selected_project)
    structure = generate_file_structure(selected_project)

    st.subheader("Préparation du repository")

    st.write("**Nom recommandé du repository :**")
    st.code(repo_name)

    st.write("**Description GitHub recommandée :**")
    st.code(repo_description)

    st.write("**Structure recommandée :**")
    st.code(structure)

    st.subheader("README généré")

    st.text_area(
        "README.md",
        value=readme,
        height=500,
    )

    st.divider()

    st.subheader("Checklist avant création")

    st.checkbox("Le nom du repository est clair")
    st.checkbox("La description est professionnelle")
    st.checkbox("Le README est adapté")
    st.checkbox("Aucune donnée personnelle sensible n’est incluse")
    st.checkbox("Le projet est prêt à être publié ou préparé localement")

    st.divider()

    st.subheader("Mission Agent GitHub")

    st.write(
        "Tu peux transformer ce plan en mission pour l’Agent GitHub. "
        "L’agent pourra ensuite préparer la création du repository, sous validation humaine."
    )

    if st.button("Créer une mission Agent GitHub depuis ce repo plan"):
        create_repo_builder_mission(
            project=selected_project,
            repo_name=repo_name,
            repo_description=repo_description,
            structure=structure,
            readme=readme,
        )

        st.success("Mission créée dans Missions Agents.")

    st.info(
        "Étape future : connecter l’API GitHub pour créer le repository automatiquement après validation."
    )