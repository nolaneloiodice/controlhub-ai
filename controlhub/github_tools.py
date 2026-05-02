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


def generate_readme_template(repo):
    name = repo.get("name", "Nom du projet")
    description = repo.get("description") or "Description à compléter."
    language = repo.get("language") or "À préciser"
    repo_name_lower = name.lower()

    if (
        "lab" in repo_name_lower
        or "cisco" in repo_name_lower
        or "vlan" in repo_name_lower
        or "dhcp" in repo_name_lower
        or "nat" in repo_name_lower
    ):
        return f"""# {name}

## Objectif du projet

{description}

Ce lab a pour objectif de pratiquer et documenter une notion réseau à l’aide de Cisco Packet Tracer.

## Contexte

Ce projet fait partie de ma progression en réseaux dans le cadre de ma montée en compétences vers le BTS SIO option SISR.

## Technologies et outils utilisés

- Cisco Packet Tracer
- Réseaux TCP/IP
- Adressage IP
- Configuration routeur / switch
- Documentation GitHub

## Notions travaillées

- Adressage IP
- Routage
- VLAN / segmentation réseau si applicable
- DHCP si applicable
- NAT/PAT si applicable
- Diagnostic réseau
- Documentation technique

## Topologie réseau

À compléter avec une capture ou un schéma de la topologie Packet Tracer.

## Étapes de configuration

1. Création de la topologie réseau
2. Configuration des équipements
3. Attribution des adresses IP
4. Configuration des services réseau nécessaires
5. Tests de connectivité
6. Vérification du résultat

## Tests réalisés

- Ping entre les machines
- Vérification de la connectivité entre les réseaux
- Vérification du service configuré
- Analyse des erreurs éventuelles

## Résultat

À compléter avec le résultat obtenu et les captures importantes.

## Compétences développées

- Compréhension des bases réseau
- Configuration Cisco Packet Tracer
- Diagnostic de connectivité
- Documentation technique
- Organisation d’un lab réseau

## Améliorations possibles

- Ajouter des captures d’écran
- Ajouter une explication plus détaillée de la topologie
- Ajouter une section troubleshooting
- Ajouter des commandes utilisées
- Ajouter une conclusion technique
"""

    if "controlhub" in repo_name_lower:
        return f"""# {name}

## Présentation

{description}

ControlHub AI est un centre de contrôle personnel en développement, conçu pour centraliser l’apprentissage, les projets, les objectifs, les notes, les missions agents et les futures automatisations IA.

## Objectifs

- Suivre mes compétences
- Centraliser mes projets
- Organiser mes objectifs
- Documenter mes apprentissages
- Piloter des agents IA locaux
- Préparer de futures intégrations GitHub, email, LinkedIn et calendrier

## Fonctionnalités actuelles

- Dashboard Streamlit
- Command Center
- Missions Agents
- Gestion des compétences
- Gestion des projets
- Gestion des objectifs
- Roadmap
- Session du jour
- Notes / Learning Log
- Assistant IA local
- Connecteur GitHub en lecture seule

## Architecture

controlhub-ai/
├── app.py
├── controlhub/
│   ├── agents.py
│   ├── github_tools.py
│   ├── storage.py
│   └── pages/
├── data/
├── docs/
└── requirements.txt

## Stack technique

- Python
- Streamlit
- JSON
- Git / GitHub
- Requests

## Roadmap

- Ajouter un connecteur GitHub plus avancé
- Générer des README automatiquement
- Ajouter des brouillons LinkedIn
- Ajouter des brouillons email
- Connecter une vraie IA
- Ajouter des agents spécialisés
- Ajouter une gestion des permissions et validations humaines

## Pourquoi ce projet ?

Je construis ControlHub AI pour apprendre en créant un outil réel, utile et évolutif.

Le projet me permet de progresser en Python, architecture logicielle, automatisation, systèmes, réseaux, cybersécurité et IA.
"""

    return f"""# {name}

## Présentation

{description}

## Objectif

Décrire ici l’objectif principal du projet.

## Technologies utilisées

- {language}
- À compléter

## Fonctionnalités

- À compléter
- À compléter
- À compléter

## Installation

Commandes d’installation à compléter.

## Utilisation

Exemple d’utilisation à compléter.

## Compétences travaillées

- Développement
- Documentation
- Organisation de projet
- Git / GitHub

## Améliorations futures

- Améliorer la documentation
- Ajouter des captures
- Ajouter des exemples
- Ajouter une roadmap
"""