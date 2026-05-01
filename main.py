import json
from pathlib import Path

DATA_DIR = Path("data")
PROFILE_FILE = DATA_DIR / "profile.json"
SKILLS_FILE = DATA_DIR / "skills.json"
PROJECTS_FILE = DATA_DIR / "projects.json"
GOALS_FILE = DATA_DIR / "goals.json"

DATA_DIR.mkdir(exist_ok=True)


def load_json(file_path, default_data):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_data


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def setup_profile():
    profile = load_json(PROFILE_FILE, {})

    if profile:
        print(f"Profil chargé : {profile.get('name', 'Utilisateur')}")
        return profile

    name = input("Ton prénom : ")
    goal = input("Ton objectif principal : ")

    profile = {
        "name": name,
        "main_goal": goal,
        "level": "amateur",
        "focus": ["Linux", "Réseaux", "Cybersécurité", "Python"]
    }

    save_json(PROFILE_FILE, profile)
    print("Profil créé avec succès.")
    return profile


def add_skill():
    skills = load_json(SKILLS_FILE, [])

    name = input("Nom de la compétence : ").strip()

    while True:
        level_input = input("Niveau actuel de 1 à 5 : ").strip()

        if level_input.isdigit():
            level = int(level_input)

            if 1 <= level <= 5:
                break

        print("Erreur : entre uniquement un nombre entre 1 et 5.")

    skill = {
        "name": name,
        "level": level
    }

    skills.append(skill)
    save_json(SKILLS_FILE, skills)
    print("Compétence ajoutée.")


def show_skills():
    skills = load_json(SKILLS_FILE, [])

    if not skills:
        print("Aucune compétence enregistrée.")
        return

    print("\nCompétences :")
    for skill in skills:
        print(f"- {skill['name']} : {skill['level']}/5")


def add_project():
    projects = load_json(PROJECTS_FILE, [])

    name = input("Nom du projet : ").strip()
    category = input("Catégorie du projet (Réseaux, Systèmes, Cyber, Python, IA...) : ").strip()
    status = input("Statut du projet (idée, en cours, terminé) : ").strip()
    github_url = input("Lien GitHub du projet : ").strip()
    description = input("Description courte du projet : ").strip()

    skills_input = input("Compétences liées au projet, séparées par des virgules : ").strip()
    skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]

    project = {
        "name": name,
        "category": category,
        "status": status,
        "skills": skills,
        "github_url": github_url,
        "description": description
    }

    projects.append(project)
    save_json(PROJECTS_FILE, projects)

    print("Projet ajouté avec succès.")


def show_projects():
    projects = load_json(PROJECTS_FILE, [])

    if not projects:
        print("Aucun projet enregistré.")
        return

    print("\nProjets enregistrés :")

    for index, project in enumerate(projects, start=1):
        print(f"\n{index}. {project['name']}")
        print(f"   Catégorie : {project['category']}")
        print(f"   Statut : {project['status']}")
        print(f"   GitHub : {project['github_url']}")
        print(f"   Description : {project['description']}")

        if project["skills"]:
            print(f"   Compétences : {', '.join(project['skills'])}")


def add_goal():
    goals = load_json(GOALS_FILE, [])

    title = input("Titre de l'objectif : ").strip()
    category = input("Catégorie (Systèmes, Réseaux, Cyber, Python, Portfolio...) : ").strip()
    priority = input("Priorité (basse, moyenne, haute) : ").strip()
    description = input("Description courte : ").strip()

    goal = {
        "title": title,
        "category": category,
        "priority": priority,
        "status": "en cours",
        "description": description
    }

    goals.append(goal)
    save_json(GOALS_FILE, goals)

    print("Objectif ajouté avec succès.")


def show_goals():
    goals = load_json(GOALS_FILE, [])

    if not goals:
        print("Aucun objectif enregistré.")
        return

    print("\nObjectifs enregistrés :")

    for index, goal in enumerate(goals, start=1):
        print(f"\n{index}. {goal['title']}")
        print(f"   Catégorie : {goal['category']}")
        print(f"   Priorité : {goal['priority']}")
        print(f"   Statut : {goal['status']}")
        print(f"   Description : {goal['description']}")


def generate_daily_task():
    skills = load_json(SKILLS_FILE, [])

    if not skills:
        print("Ajoute d'abord une compétence.")
        return

    weakest_skill = min(skills, key=lambda skill: skill["level"])

    print("\nTâche du jour :")
    print(f"Travaille 30 minutes sur : {weakest_skill['name']}")
    print("Puis écris 5 lignes dans docs/learning-log.md sur ce que tu as appris.")


def main():
    setup_profile()

    while True:
        print("\n=== ControlHub AI ===")
        print("1. Voir mes compétences")
        print("2. Ajouter une compétence")
        print("3. Générer ma tâche du jour")
        print("4. Voir mes projets")
        print("5. Ajouter un projet")
        print("6. Voir mes objectifs")
        print("7. Ajouter un objectif")
        print("8. Quitter")

        choice = input("Choix : ")

        if choice == "1":
            show_skills()
        elif choice == "2":
            add_skill()
        elif choice == "3":
            generate_daily_task()
        elif choice == "4":
            show_projects()
        elif choice == "5":
            add_project()
        elif choice == "6":
            show_goals()
        elif choice == "7":
            add_goal()
        elif choice == "8":
            print("À bientôt.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()