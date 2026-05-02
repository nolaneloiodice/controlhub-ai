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