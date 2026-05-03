import re
from pathlib import Path

import streamlit as st

from controlhub.action_log_tools import add_action_log
from controlhub.ai_tools import (
    generate_ai_response,
    get_ollama_models,
    get_recommended_model,
)
from controlhub.storage import (
    AGENT_TASKS_FILE,
    LEARNING_LOG_FILE,
    TASKS_FILE,
    load_all_data,
    load_json,
    save_json,
)


DEV_PROPOSALS_DIR = Path("dev_proposals")


CONTROLHUB_MODULES = """
Modules existants dans ControlHub AI :
- app.py : routeur principal Streamlit et App Shell
- controlhub/pages/pilot.py : pilotage central
- controlhub/pages/today.py : cockpit quotidien
- controlhub/pages/ai_assistant.py : assistant IA local
- controlhub/pages/missions.py : missions agents
- controlhub/pages/tasks.py : tâches / planning
- controlhub/pages/action_log.py : journal d'activité
- controlhub/pages/dev_workshop.py : atelier de développement IA supervisé
- controlhub/pages/memory.py : mémoire locale
- controlhub/pages/github.py : connecteur GitHub lecture seule
- controlhub/pages/repo_builder.py : préparation de repositories GitHub
- controlhub/pages/projects.py : gestion des projets
- controlhub/pages/goals.py : gestion des objectifs
- controlhub/pages/notes.py : notes / learning log
- controlhub/pages/daily_session.py : session du jour
- controlhub/ai_tools.py : couche IA locale Ollama / OpenAI optionnel
- controlhub/action_log_tools.py : journalisation
- controlhub/storage.py : chemins fichiers et JSON
- controlhub/memory_tools.py : mémoire personnelle locale
"""


DEV_AGENT_RULES = """
Règles strictes de l'Agent Développeur ControlHub :
- Ne jamais prétendre avoir modifié un fichier si tu proposes seulement une modification.
- Ne jamais inventer une fonctionnalité existante.
- Toujours distinguer : ce qui existe déjà, ce qui est proposé, ce qui doit être vérifié.
- Toujours citer les fichiers probablement concernés.
- Toujours expliquer l'impact exact sur ControlHub AI.
- Toujours signaler les risques possibles : bugs Streamlit, clés dupliquées, JSON, navigation, imports, données privées.
- Ne jamais chercher sur Internet sans validation humaine.
- Si une information externe est nécessaire, demander à Nolane de fournir ou valider la source.
- Ne jamais proposer d'action irréversible sans sauvegarde.
- Préférer les fichiers complets à remplacer quand c'est plus sûr.
- Répondre en français, de manière claire, directe et actionnable.
- Dialoguer avec Nolane si la demande est floue.
- Se comporter comme un assistant développeur supervisé, pas comme un simple générateur de texte.
"""


TARGET_FILES = [
    "Auto / à déterminer",
    "app.py",
    "controlhub/pages/pilot.py",
    "controlhub/pages/today.py",
    "controlhub/pages/ai_assistant.py",
    "controlhub/pages/missions.py",
    "controlhub/pages/tasks.py",
    "controlhub/pages/action_log.py",
    "controlhub/pages/dev_workshop.py",
    "controlhub/pages/memory.py",
    "controlhub/pages/github.py",
    "controlhub/pages/repo_builder.py",
    "controlhub/pages/projects.py",
    "controlhub/pages/goals.py",
    "controlhub/pages/notes.py",
    "controlhub/pages/daily_session.py",
    "controlhub/ai_tools.py",
    "controlhub/action_log_tools.py",
    "controlhub/storage.py",
    "controlhub/memory_tools.py",
    "Nouveau fichier",
]


def infer_request_type(request):
    text = request.lower()

    if any(word in text for word in ["bug", "erreur", "corrige", "crash", "ne marche pas"]):
        return "Correction bug"

    if any(word in text for word in ["interface", "ui", "design", "simple", "intuitif", "application"]):
        return "Amélioration UI"

    if any(word in text for word in ["refactor", "nettoyer", "simplifier le code", "réorganiser"]):
        return "Refactor"

    if any(word in text for word in ["agent", "orchestrateur", "ia", "assistant", "auto améliore"]):
        return "Agent IA"

    if any(word in text for word in ["github", "linkedin", "email", "mail", "api", "connecteur"]):
        return "Connecteur externe"

    if any(word in text for word in ["automatiser", "workflow", "automatisation"]):
        return "Automatisation"

    if any(word in text for word in ["sécurité", "permission", "validation", "rollback", "sauvegarde"]):
        return "Sécurité / permissions"

    if any(word in text for word in ["rapide", "performance", "lent", "optimiser"]):
        return "Performance"

    return "Nouvelle fonctionnalité"


def build_dev_prompt(request, external_context):
    detected_type = infer_request_type(request)

    return f"""
Tu es l'Agent Développeur ControlHub.

Tu travailles avec Nolane pour améliorer ControlHub AI lui-même.

Demande de Nolane :
{request}

Type détecté automatiquement :
{detected_type}

Contexte externe fourni par Nolane :
{external_context if external_context.strip() else "Aucun contexte externe fourni."}

{CONTROLHUB_MODULES}

{DEV_AGENT_RULES}

Tu dois répondre avec cette structure :

## 1. Ce que j'ai compris
Reformule clairement la demande.

## 2. Type de demande détecté
Explique pourquoi tu classes cette demande dans ce type.

## 3. Impact exact sur ControlHub AI
Explique ce que cela changerait dans l'application.

## 4. Fichiers probablement concernés
Liste les fichiers concernés et pourquoi.

## 5. Plan technique proposé
Donne un plan clair en étapes.

## 6. Points à clarifier avec Nolane
Pose des questions seulement si c'est nécessaire. Sinon écris "Aucune clarification indispensable."

## 7. Risques / points d'attention
Indique les risques techniques possibles.

## 8. Tests à faire
Liste les tests à effectuer dans l'interface.

## 9. Prochaine action recommandée
Dis exactement ce qu'il faut faire ensuite.
"""


def build_file_generation_prompt(
    request,
    analysis,
    target_file,
    file_goal,
    external_context,
):
    detected_type = infer_request_type(request)

    return f"""
Tu es l'Agent Développeur ControlHub.

Tu dois générer un fichier complet proposé pour ControlHub AI.

IMPORTANT :
- Tu ne modifies pas réellement le projet.
- Tu génères uniquement le contenu complet d'un fichier proposé.
- Tu dois produire uniquement le contenu du fichier.
- Ne mets pas de bloc Markdown.
- Ne mets pas ```python.
- Ne mets pas d'explication avant ou après.
- Le fichier doit être cohérent avec l'architecture actuelle.
- Le code doit être complet, propre et utilisable.
- Respecte les imports existants et les conventions du projet.
- Attention aux clés Streamlit uniques.
- Attention aux fichiers JSON privés.
- Attention à ne pas inventer des fonctions qui n'existent pas.

Demande initiale :
{request}

Type détecté automatiquement :
{detected_type}

Fichier cible ou type de fichier :
{target_file}

Objectif précis du fichier :
{file_goal}

Analyse précédente de l'Agent Développeur :
{analysis}

Contexte externe fourni :
{external_context if external_context.strip() else "Aucun contexte externe fourni."}

Modules existants :
{CONTROLHUB_MODULES}

Génère maintenant le contenu complet du fichier proposé.
"""


def ensure_dev_proposals_dir():
    DEV_PROPOSALS_DIR.mkdir(exist_ok=True)


def sanitize_filename(filename):
    filename = filename.strip()

    if not filename:
        return "proposal.txt"

    filename = filename.replace("\\", "_").replace("/", "_")
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)

    if "." not in filename:
        filename += ".txt"

    return filename


def clean_generated_file_content(content):
    cleaned = content.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    return cleaned + "\n"


def save_proposed_file(filename, content):
    ensure_dev_proposals_dir()

    safe_filename = sanitize_filename(filename)
    file_path = DEV_PROPOSALS_DIR / safe_filename

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path


def create_dev_task(request, analysis):
    tasks = load_json(TASKS_FILE, [])
    request_type = infer_request_type(request)

    title = f"Dev ControlHub — {request_type}"

    description = f"""Demande :
{request}

Type détecté :
{request_type}

Analyse Agent Développeur :
{analysis}
"""

    tasks.append(
        {
            "title": title,
            "category": "ControlHub AI",
            "priority": "haute",
            "status": "à faire",
            "linked_project": "ControlHub AI",
            "linked_agent": "Agent Développeur ControlHub",
            "due_date": "",
            "description": description,
        }
    )

    save_json(TASKS_FILE, tasks)

    add_action_log(
        source="Atelier Dev IA",
        action_type="Création tâche dev",
        title=title,
        details=description,
    )


def create_dev_mission(request, analysis):
    missions = load_json(AGENT_TASKS_FILE, [])
    request_type = infer_request_type(request)

    title = f"Agent Développeur — {request_type}"

    context = f"""Demande :
{request}

Type détecté :
{request_type}

Analyse :
{analysis}

Règles :
- Ne rien appliquer sans validation humaine.
- Expliquer les fichiers concernés.
- Préparer des fichiers complets si nécessaire.
- Journaliser les actions.
"""

    missions.append(
        {
            "agent": "Agent Développeur ControlHub",
            "title": title,
            "priority": "haute",
            "status": "à faire",
            "context": context,
        }
    )

    save_json(AGENT_TASKS_FILE, missions)

    add_action_log(
        source="Atelier Dev IA",
        action_type="Création mission dev",
        title=title,
        details=context,
    )


def save_dev_analysis_to_notes(request, analysis):
    request_type = infer_request_type(request)

    note = f"""

## Analyse Agent Développeur — {request_type}

### Demande

{request}

### Analyse

{analysis}
"""

    with open(LEARNING_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(note)

    add_action_log(
        source="Atelier Dev IA",
        action_type="Création note dev",
        title=f"Analyse dev — {request_type}",
        details=note,
    )


def render_file_proposal_section(
    request,
    analysis,
    external_context,
    profile,
    skills,
    projects,
    goals,
    selected_model,
):
    st.divider()

    st.subheader("🧪 Génération de fichier proposé")

    st.warning(
        "Cette section génère un fichier dans `dev_proposals/`. "
        "Elle ne modifie pas encore le vrai code de ControlHub AI."
    )

    target_file = st.selectbox(
        "Fichier cible",
        TARGET_FILES,
        key="dev-target-file",
    )

    proposed_filename = st.text_input(
        "Nom du fichier proposé",
        value="proposal.py",
        help="Exemple : pilot_proposal.py, today_v2.py, ai_tools_refactor.py",
    )

    file_goal = st.text_area(
        "Objectif précis du fichier à générer",
        placeholder=(
            "Exemple : Générer une version complète proposée de pilot.py avec une meilleure compréhension des demandes, "
            "journalisation et boutons Streamlit avec clés uniques."
        ),
        height=120,
    )

    if st.button("Générer un fichier proposé", key="dev-generate-proposed-file"):
        if not file_goal.strip():
            st.error("Décris l’objectif précis du fichier à générer.")
            return

        prompt = build_file_generation_prompt(
            request=request,
            analysis=analysis,
            target_file=target_file,
            file_goal=file_goal,
            external_context=external_context,
        )

        with st.spinner("Génération du fichier proposé en cours..."):
            generated_content = generate_ai_response(
                prompt,
                profile,
                skills,
                projects,
                goals,
                model_name=selected_model,
                task_type="code",
                response_style="Détaillé",
            )

        cleaned_content = clean_generated_file_content(generated_content)
        file_path = save_proposed_file(proposed_filename, cleaned_content)

        st.session_state["dev_last_proposed_file_path"] = str(file_path)
        st.session_state["dev_last_proposed_file_content"] = cleaned_content

        add_action_log(
            source="Atelier Dev IA",
            action_type="Fichier proposé généré",
            title=f"Proposition : {file_path}",
            details=(
                f"Demande :\n{request}\n\n"
                f"Fichier cible : {target_file}\n"
                f"Objectif :\n{file_goal}\n\n"
                f"Fichier généré : {file_path}"
            ),
        )

        st.success(f"Fichier proposé généré : {file_path}")

    if "dev_last_proposed_file_content" in st.session_state:
        st.subheader("Dernier fichier proposé")

        st.write(f"**Chemin :** {st.session_state['dev_last_proposed_file_path']}")

        st.text_area(
            "Contenu généré",
            value=st.session_state["dev_last_proposed_file_content"],
            height=500,
        )

        st.info(
            "Pour l’instant, copie/colle manuellement ce contenu dans le vrai fichier seulement si tu valides."
        )


def render_dev_workshop_page():
    profile, skills, projects, goals = load_all_data()

    st.title("🛠️ Atelier Dev IA")

    st.write(
        "Décris ce que tu veux améliorer. L’Agent Développeur analyse, choisit le type de demande, "
        "propose un plan, puis prépare les actions utiles."
    )

    st.info(
        "Objectif : moins de menus, plus d’intelligence. Tu demandes, ControlHub analyse et te guide."
    )

    st.divider()

    request = st.text_area(
        "Que veux-tu améliorer dans ControlHub AI ?",
        placeholder=(
            "Exemples :\n"
            "- Je veux que l’interface ressemble plus à une application qu’à un site.\n"
            "- Je veux que l’agent central choisisse seul le bon workflow.\n"
            "- Je veux ajouter une sauvegarde avant modification automatique.\n"
            "- Je veux que l’Atelier Dev IA génère un fichier complet proposé."
        ),
        height=190,
    )

    detected_type = infer_request_type(request) if request.strip() else "En attente"
    st.caption(f"Type détecté automatiquement : {detected_type}")

    external_context = st.text_area(
        "Contexte ou source externe fournie par toi",
        placeholder=(
            "Colle ici une documentation, une erreur, une source web, un extrait de code, "
            "ou une précision. L’agent peut demander une source, mais ne doit pas chercher sans validation."
        ),
        height=120,
    )

    selected_model = None
    response_style = "Normal"

    with st.expander("Réglages avancés"):
        available_models = get_ollama_models()

        if available_models:
            recommended_model = get_recommended_model(
                task_type="code",
                available_models=available_models,
            )

            model_options = ["Auto"] + available_models

            selected_model_choice = st.selectbox(
                "Modèle IA local",
                model_options,
                index=0,
            )

            if selected_model_choice == "Auto":
                selected_model = recommended_model
                st.info(f"Mode Auto : l’Atelier Dev IA utilisera probablement {recommended_model}.")
            else:
                selected_model = selected_model_choice

        response_style = st.selectbox(
            "Niveau de détail",
            [
                "Rapide",
                "Normal",
                "Détaillé",
            ],
            index=1,
        )

    st.divider()

    if st.button("Analyser ma demande", key="dev-workshop-analyze"):
        if not request.strip():
            st.error("Décris d’abord l’amélioration souhaitée.")
            return

        prompt = build_dev_prompt(request, external_context)

        with st.spinner("Analyse de l’Agent Développeur en cours..."):
            analysis = generate_ai_response(
                prompt,
                profile,
                skills,
                projects,
                goals,
                model_name=selected_model,
                task_type="code",
                response_style=response_style,
            )

        st.session_state["dev_last_request"] = request
        st.session_state["dev_last_external_context"] = external_context
        st.session_state["dev_last_analysis"] = analysis
        st.session_state["dev_last_selected_model"] = selected_model

        add_action_log(
            source="Atelier Dev IA",
            action_type="Analyse dev IA",
            title=f"Analyse dev — {infer_request_type(request)}",
            details=f"Demande :\n{request}\n\nAnalyse :\n{analysis}",
        )

    if "dev_last_analysis" in st.session_state:
        st.divider()

        st.subheader("Analyse de l’Agent Développeur")
        st.markdown(st.session_state["dev_last_analysis"])

        st.divider()

        st.subheader("Actions depuis cette analyse")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Créer une tâche dev", key="dev-create-task"):
                create_dev_task(
                    st.session_state["dev_last_request"],
                    st.session_state["dev_last_analysis"],
                )
                st.success("Tâche de développement créée.")

        with col2:
            if st.button("Créer une mission dev", key="dev-create-mission"):
                create_dev_mission(
                    st.session_state["dev_last_request"],
                    st.session_state["dev_last_analysis"],
                )
                st.success("Mission Agent Développeur créée.")

        with col3:
            if st.button("Enregistrer dans Notes", key="dev-save-note"):
                save_dev_analysis_to_notes(
                    st.session_state["dev_last_request"],
                    st.session_state["dev_last_analysis"],
                )
                st.success("Analyse enregistrée dans Notes.")

        render_file_proposal_section(
            request=st.session_state["dev_last_request"],
            analysis=st.session_state["dev_last_analysis"],
            external_context=st.session_state["dev_last_external_context"],
            profile=profile,
            skills=skills,
            projects=projects,
            goals=goals,
            selected_model=st.session_state["dev_last_selected_model"],
        )

    st.divider()

    st.subheader("🧭 Direction")

    st.write(
        "Prochaine étape : créer un Agent Orchestrateur global qui choisira automatiquement "
        "le bon workflow, le bon agent et le bon modèle depuis Pilotage."
    )