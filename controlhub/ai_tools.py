import os
from pathlib import Path

import requests
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from controlhub.memory_tools import format_memory_for_ai


load_dotenv()
load_dotenv(Path("controlhub") / ".env", override=False)


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


def find_model_by_keywords(models, keywords):
    for model in models:
        model_lower = model.lower()

        for keyword in keywords:
            if keyword.lower() in model_lower:
                return model

    return None


def get_recommended_model(task_type="general", available_models=None):
    models = available_models or get_ollama_models()

    if not models:
        return get_ollama_model()

    task_type = task_type.lower()

    if task_type in ["code", "debug", "python", "github", "readme"]:
        coder_model = find_model_by_keywords(
            models,
            ["qwen2.5-coder", "coder", "code"],
        )
        if coder_model:
            return coder_model

    general_model = find_model_by_keywords(
        models,
        ["llama3.2:3b", "llama3.2", "llama"],
    )

    if general_model:
        return general_model

    return models[0]


def get_response_style_instruction(response_style):
    style = response_style.lower()

    if style in ["rapide", "fast"]:
        return """
Style de réponse :
- Réponse courte.
- Maximum 8 à 12 lignes.
- Une seule priorité principale.
- Pas d'explication inutile.
- Donne directement les actions à faire.
"""

    if style in ["détaillé", "detaille", "detailed"]:
        return """
Style de réponse :
- Réponse détaillée.
- Explique le raisonnement.
- Donne un plan structuré.
- Ajoute les risques, limites et prochaines étapes.
"""

    return """
Style de réponse :
- Réponse structurée.
- Sois clair et pratique.
- Donne un plan actionnable.
- Évite les longs paragraphes inutiles.
"""


def get_num_predict(response_style):
    style = response_style.lower()

    if style in ["rapide", "fast"]:
        return 350

    if style in ["détaillé", "detaille", "detailed"]:
        return 1200

    return 700


def build_context(profile, skills, projects, goals):
    context_lines = []

    context_lines.append("Profil utilisateur :")
    context_lines.append(f"- Nom : {profile.get('name', 'Utilisateur')}")
    context_lines.append(
        f"- Objectif principal : {profile.get('main_goal', 'Non défini')}"
    )

    context_lines.append("\nModules ControlHub AI déjà existants :")
    context_lines.append("- Accueil")
    context_lines.append("- Aujourd'hui")
    context_lines.append("- Command Center")
    context_lines.append("- Missions Agents")
    context_lines.append("- Tâches / Planning")
    context_lines.append("- GitHub")
    context_lines.append("- Repo Builder")
    context_lines.append("- Compétences")
    context_lines.append("- Projets")
    context_lines.append("- Objectifs")
    context_lines.append("- Roadmap")
    context_lines.append("- Session du jour")
    context_lines.append("- Notes")
    context_lines.append("- Assistant IA")
    context_lines.append("- Mémoire")

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

ControlHub AI est le centre de contrôle personnel de Nolane.
Tu dois aider à organiser sa vie, ses projets, son apprentissage, ses objectifs, ses tâches, ses missions agents, GitHub, LinkedIn, emails, planning et automatisations.

Règles importantes :
- ControlHub AI est un outil personnel déjà existant.
- Ne parle pas d'utilisateurs sauf si Nolane demande de transformer ControlHub AI en produit public.
- Par défaut, parle de "toi", "ton panel", "ton usage personnel".
- Ne propose pas Trello, Asana, Notion ou d'autres outils externes comme première solution.
- Privilégie les modules internes de ControlHub AI.
- Ne dis jamais de créer un module qui existe déjà.
- Si une fonctionnalité existe déjà, propose de l'utiliser ou de l'améliorer.
- Si une fonctionnalité n'existe pas encore, dis clairement "à créer" ou "future évolution".
- Ne jamais inventer de forum, communauté, bouton, intégration ou fonctionnalité inexistante.
- Toujours distinguer : ce qui existe déjà, ce qui est en cours, ce qui est une idée future.
- Donne des actions réalisables directement dans le panel actuel.
- Évite les phrases vagues comme "consulte les ressources officielles" sans action concrète.
- Pour chaque recommandation, propose une action courte, utile et vérifiable.
- Ne prétends jamais avoir exécuté une action externe si tu as seulement rédigé une proposition.

Ton rôle :
- aider Nolane à progresser en BTS SIO SISR, systèmes, réseaux, cybersécurité, Python et IA ;
- transformer ses projets en actions concrètes ;
- aider à préparer GitHub, LinkedIn, emails, entretiens, notes et décisions ;
- utiliser la mémoire personnelle pour adapter tes réponses ;
- proposer des choix optimisés, mais toujours expliquer simplement ;
- rester prudent avec toute action externe.

Réponds en français.
Sois direct, pratique, structuré et orienté action.
"""


def generate_with_ollama(prompt, model_name=None, response_style="normal"):
    url = f"{get_ollama_base_url()}/api/generate"

    selected_model = model_name or get_ollama_model()

    payload = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0.4,
            "num_predict": get_num_predict(response_style),
        },
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

Utilise Ollama en local ou ajoute OPENAI_API_KEY dans .env.
"""

    if OpenAI is None:
        return """### Package OpenAI manquant

Installe le package avec :

py -m pip install openai
"""

    client = OpenAI()

    response = client.responses.create(
        model=get_openai_model(),
        instructions=build_system_prompt(),
        input=prompt,
    )

    return response.output_text


def generate_ai_response(
    user_prompt,
    profile,
    skills,
    projects,
    goals,
    model_name=None,
    task_type="general",
    response_style="normal",
):
    context = build_context(profile, skills, projects, goals)
    system_prompt = build_system_prompt()
    style_instruction = get_response_style_instruction(response_style)

    provider = get_ai_provider()

    if provider == "ollama":
        selected_model = model_name or get_recommended_model(task_type)
    else:
        selected_model = model_name

    final_prompt = f"""
{system_prompt}

{style_instruction}

Contexte ControlHub AI :

{context}

Demande utilisateur :

{user_prompt}
"""

    try:
        if provider == "ollama":
            if not is_ollama_available():
                return """### Ollama non disponible

ControlHub AI est configuré pour utiliser Ollama, mais Ollama ne répond pas.

Vérifie :
1. qu’Ollama est lancé ;
2. que le modèle est installé ;
3. que OLLAMA_BASE_URL=http://localhost:11434 est dans .env.

Commande utile :

ollama run llama3.2:3b
"""
            return generate_with_ollama(
                final_prompt,
                model_name=selected_model,
                response_style=response_style,
            )

        if provider == "openai":
            return generate_with_openai(final_prompt)

        return """### Fournisseur IA invalide

Dans .env, utilise :

AI_PROVIDER=ollama

ou

AI_PROVIDER=openai
"""

    except Exception as error:
        return f"""### Erreur IA

Impossible de générer une réponse.

Détail technique :

{error}
"""