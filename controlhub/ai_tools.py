import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

from controlhub.memory_tools import format_memory_for_ai


load_dotenv()


def get_ai_provider():
    return os.getenv("AI_PROVIDER", "ollama").lower()


def get_ollama_model():
    return os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def get_ollama_base_url():
    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def get_openai_model():
    return os.getenv("OPENAI_MODEL", "gpt-5.5")


def is_openai_configured():
    return bool(os.getenv("OPENAI_API_KEY"))


def is_ollama_available():
    try:
        response = requests.get(
            f"{get_ollama_base_url()}/api/tags",
            timeout=5,
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_ollama_models():
    try:
        response = requests.get(
            f"{get_ollama_base_url()}/api/tags",
            timeout=5,
        )

        if response.status_code != 200:
            return []

        data = response.json()
        models = data.get("models", [])

        return [model.get("name") for model in models if model.get("name")]

    except requests.RequestException:
        return []


def get_ai_status():
    provider = get_ai_provider()

    if provider == "ollama":
        if is_ollama_available():
            return "IA locale Ollama connectée."
        return "Ollama non disponible. Vérifie qu’Ollama est lancé."

    if provider == "openai":
        if is_openai_configured():
            return "IA OpenAI connectée."
        return "OpenAI non configuré. Ajoute OPENAI_API_KEY dans .env."

    return "Aucun fournisseur IA valide configuré."


def build_context(profile, skills, projects, goals):
    context_lines = []

    context_lines.append("Profil utilisateur :")
    context_lines.append(f"- Nom : {profile.get('name', 'Utilisateur')}")
    context_lines.append(
        f"- Objectif principal : {profile.get('main_goal', 'Non défini')}"
    )

    context_lines.append("\nCompétences suivies :")
    if skills:
        for skill in skills:
            context_lines.append(
                f"- {skill.get('name', 'Compétence')} : {skill.get('level', 1)}/5"
            )
    else:
        context_lines.append("- Aucune compétence enregistrée")

    context_lines.append("\nProjets enregistrés :")
    if projects:
        for project in projects:
            context_lines.append(
                f"- {project.get('name', 'Projet')} "
                f"({project.get('category', 'Catégorie non définie')}) "
                f"- statut : {project.get('status', 'Non défini')}"
            )
    else:
        context_lines.append("- Aucun projet enregistré")

    context_lines.append("\nObjectifs actifs :")
    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]

    if active_goals:
        for goal in active_goals:
            context_lines.append(
                f"- {goal.get('title', 'Objectif')} "
                f"- priorité : {goal.get('priority', 'Non définie')} "
                f"- catégorie : {goal.get('category', 'Non définie')}"
            )
    else:
        context_lines.append("- Aucun objectif actif")

    context_lines.append("\n")
    context_lines.append(format_memory_for_ai())

    return "\n".join(context_lines)


def build_system_prompt():
    return """
Tu es l'assistant IA local intégré de ControlHub AI.

Ton rôle :
- aider l'utilisateur à organiser sa vie, ses projets, ses objectifs et son apprentissage ;
- comprendre que ControlHub AI doit devenir le centre principal, pas seulement recommander des outils externes ;
- privilégier les solutions intégrées dans ControlHub AI quand c’est cohérent ;
- éviter de proposer Trello, Asana, Notion ou autres outils externes comme première solution, sauf si l'utilisateur le demande ;
- proposer des évolutions concrètes du panel plutôt que de déléguer l'organisation à une autre plateforme ;
- l’aider à progresser en BTS SIO SISR, systèmes, réseaux, cybersécurité, Python et IA ;
- transformer ses projets en actions concrètes ;
- aider à préparer GitHub, LinkedIn, emails, entretiens, notes et décisions ;
- utiliser la mémoire personnelle pour adapter tes réponses ;
- proposer des choix optimisés, mais toujours expliquer simplement ;
- rester prudent avec toute action externe ;
- ne jamais prétendre avoir exécuté une action si tu as seulement rédigé une proposition.
- ne jamais inventer de plateforme, forum, communauté ou fonctionnalité qui n’existe pas encore ;
- si une fonctionnalité n’existe pas encore dans ControlHub AI, proposer de la créer comme module futur ;
- toujours distinguer : ce qui existe déjà, ce qui est en cours, ce qui est une idée future ;
- donner des actions réalisables directement dans le panel actuel ;
- éviter les phrases vagues comme "consulte les ressources officielles" sans préciser quoi faire concrètement ;
- pour chaque recommandation, proposer une action courte, utile et vérifiable ;
- tu dois considérer que ControlHub AI est un outil personnel déjà existant avec des modules réels. Ne propose jamais une action qui suppose une fonctionnalité inexistante. Si une fonctionnalité n’existe pas, formule-la comme “à créer” et propose une étape de développement concrète.
- ne parle pas d’“utilisateurs” sauf si l’utilisateur demande de transformer ControlHub AI en produit public. Par défaut, parle de “toi”, “ton panel”, “ton usage personnel”.
Réponds en français.
Sois direct, pratique, structuré et orienté action.
"""


def generate_with_ollama(prompt, model_name=None):
    url = f"{get_ollama_base_url()}/api/generate"

    selected_model = model_name or get_ollama_model()

    payload = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(url, json=payload, timeout=180)

    if response.status_code != 200:
        raise Exception(f"Erreur Ollama : {response.status_code} - {response.text}")

    data = response.json()
    return data.get("response", "")


def generate_with_openai(prompt):
    if not is_openai_configured():
        return """### OpenAI non configuré

Aucune clé API OpenAI n’a été trouvée.

Utilise Ollama en local ou ajoute `OPENAI_API_KEY` dans `.env`.
"""

    client = OpenAI()

    response = client.responses.create(
        model=get_openai_model(),
        instructions=build_system_prompt(),
        input=prompt,
    )

    return response.output_text


def generate_ai_response(user_prompt, profile, skills, projects, goals, model_name=None):
    context = build_context(profile, skills, projects, goals)
    system_prompt = build_system_prompt()

    final_prompt = f"""
{system_prompt}

Contexte ControlHub AI :

{context}

Demande utilisateur :

{user_prompt}
"""

    provider = get_ai_provider()

    try:
        if provider == "ollama":
            if not is_ollama_available():
                return """### Ollama non disponible

ControlHub AI est configuré pour utiliser Ollama, mais Ollama ne répond pas.

Vérifie :
1. qu’Ollama est lancé ;
2. que le modèle est installé ;
3. que `OLLAMA_BASE_URL=http://localhost:11434` est dans `.env`.

Commande utile :

`ollama run llama3.2:3b`
"""
            return generate_with_ollama(final_prompt, model_name=model_name)

        if provider == "openai":
            return generate_with_openai(final_prompt)

        return """### Fournisseur IA invalide

Dans `.env`, utilise :

`AI_PROVIDER=ollama`

ou

`AI_PROVIDER=openai`
"""

    except Exception as error:
        return f"""### Erreur IA

Impossible de générer une réponse.

Détail technique :

{error}
"""