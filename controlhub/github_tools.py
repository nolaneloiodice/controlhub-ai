import requests


GITHUB_API_BASE_URL = "https://api.github.com"


def get_public_repositories(username):
    """
    Récupère les repositories publics d'un utilisateur GitHub.

    Cette fonction est en lecture seule.
    Elle ne modifie rien sur GitHub.
    """
    url = f"{GITHUB_API_BASE_URL}/users/{username}/repos"

    params = {
        "sort": "updated",
        "direction": "desc",
        "per_page": 100,
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(
            f"Erreur GitHub API : {response.status_code} - {response.text}"
        )

    repositories = response.json()
    cleaned_repositories = []

    for repo in repositories:
        cleaned_repositories.append(
            {
                "name": repo.get("name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
                "url": repo.get("html_url"),
                "updated_at": repo.get("updated_at"),
                "is_fork": repo.get("fork"),
            }
        )

    return cleaned_repositories


def generate_repository_suggestions(repo):
    suggestions = []

    if not repo.get("description"):
        suggestions.append("Ajouter une description courte au repository.")

    if not repo.get("language"):
        suggestions.append("Vérifier que le langage principal est bien détecté.")

    if repo.get("is_fork"):
        suggestions.append(
            "Indiquer clairement que ce repository est un fork si tu le conserves sur ton profil."
        )

    name = repo.get("name", "").lower()

    if (
        "lab" in name
        or "cisco" in name
        or "vlan" in name
        or "dhcp" in name
        or "nat" in name
    ):
        suggestions.append("Ajouter une section Objectif du lab.")
        suggestions.append("Ajouter une section Topologie réseau.")
        suggestions.append("Ajouter une section Étapes de configuration.")
        suggestions.append("Ajouter une section Compétences travaillées.")
        suggestions.append("Ajouter des captures Packet Tracer si possible.")

    if "controlhub" in name:
        suggestions.append("Ajouter une roadmap claire du projet.")
        suggestions.append("Ajouter une section Architecture.")
        suggestions.append("Ajouter une section Fonctionnalités actuelles.")
        suggestions.append("Ajouter une section Prochaines intégrations prévues.")

    if not suggestions:
        suggestions.append(
            "Vérifier que le README explique clairement l’objectif, l’installation et l’utilisation du projet."
        )

    return suggestions