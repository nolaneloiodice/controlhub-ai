import json
from pathlib import Path

DATA_DIR = Path("data")
PROFILE_FILE = DATA_DIR / "profile.json"
SKILLS_FILE = DATA_DIR / "skills.json"

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

    name = input("Nom de la compétence : ")
    level = input("Niveau actuel de 1 à 5 : ")

    skill = {
        "name": name,
        "level": int(level)
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
        print("4. Quitter")

        choice = input("Choix : ")

        if choice == "1":
            show_skills()
        elif choice == "2":
            add_skill()
        elif choice == "3":
            generate_daily_task()
        elif choice == "4":
            print("À bientôt.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()