def get_priority_goal(goals):
    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]

    high_priority_goals = [
        goal for goal in active_goals
        if goal.get("priority", "").lower() == "haute"
    ]

    if high_priority_goals:
        return high_priority_goals[0]

    if active_goals:
        return active_goals[0]

    return None


def generate_day_plan(priority_goal):
    lines = []

    lines.append("### Plan de journée recommandé")

    if priority_goal:
        lines.append(f"**Priorité principale :** {priority_goal.get('title')}")
        lines.append(priority_goal.get("description", ""))

    lines.extend(
        [
            "1. Faire une session concentrée de 45 à 90 minutes.",
            "2. Travailler sur une seule priorité.",
            "3. Noter ce qui a été fait dans le learning log.",
            "4. Faire un petit commit Git si le projet a avancé.",
            "5. Préparer la prochaine action.",
        ]
    )

    return "\n\n".join(lines)


def generate_priority_task(priority_goal):
    if not priority_goal:
        return (
            "Aucun objectif actif trouvé. "
            "Ajoute un objectif dans l’onglet Objectifs pour générer une tâche prioritaire."
        )

    return f"""### Tâche prioritaire

**{priority_goal.get('title', 'Objectif prioritaire')}**

{priority_goal.get('description', '')}

Travaille 60 minutes sur cet objectif. À la fin, écris une note courte avec :
- ce que tu as fait
- ce que tu as compris
- ce qui bloque
- la prochaine action
"""


def generate_progress_summary(profile, skills, projects, goals):
    active_goals = [goal for goal in goals if goal.get("status") != "terminé"]

    name = profile.get("name", "Nolane")
    main_goal = profile.get("main_goal", "progresser en IT/cyber")

    lines = [
        "### Résumé de progression",
        f"**Profil :** {name}",
        f"**Objectif principal :** {main_goal}",
        f"**Compétences suivies :** {len(skills)}",
        f"**Projets enregistrés :** {len(projects)}",
        f"**Objectifs actifs :** {len(active_goals)}",
    ]

    if projects:
        lines.append("### Projets clés")
        for project in projects[:5]:
            lines.append(
                f"- **{project.get('name', 'Projet')}** "
                f"({project.get('category', 'Catégorie non définie')})"
            )

    return "\n\n".join(lines)


def generate_linkedin_post():
    return """### Brouillon LinkedIn

Je continue à construire **ControlHub AI**, mon centre de contrôle personnel pour organiser ma progression en informatique.

L’objectif est de centraliser mes compétences, mes projets, mes objectifs, mes notes et mes prochaines actions dans un dashboard Python.

Ce projet me permet d’apprendre en construisant, tout en renforçant des compétences importantes pour mon parcours BTS SIO SISR :
- systèmes et réseaux
- Linux
- cybersécurité
- Python
- Git/GitHub
- documentation technique
- organisation de projet

Prochaine étape : faire évoluer ControlHub AI vers un véritable panel multi-agents capable de m’assister sur GitHub, les emails, LinkedIn, l’apprentissage et l’organisation quotidienne.
"""


def generate_followup_email():
    return """### Brouillon email

Bonjour,

Je me permets de revenir vers vous à la suite de notre échange concernant ma recherche d’alternance pour le BTS SIO option SISR.

Depuis notre rencontre, j’ai continué à structurer ma montée en compétences en systèmes, réseaux et cybersécurité. J’ai notamment avancé sur mes labs réseaux documentés sur GitHub et sur un projet personnel en Python, ControlHub AI, qui me permet de suivre mes compétences, projets, objectifs et notes d’apprentissage.

Je reste disponible pour un entretien ou tout échange complémentaire.

Cordialement,  
Nolane Loiodice
"""


def generate_github_improvements():
    return """### Améliorations GitHub recommandées

1. Ajouter une description claire à chaque repository.
2. Améliorer les README avec : objectif, topologie, notions, étapes, résultat.
3. Ajouter des captures ou schémas quand c’est possible.
4. Ajouter une section “Compétences travaillées”.
5. Mettre en avant ControlHub AI comme projet central.
"""


def generate_tryhackme_session():
    return """### Session TryHackMe recommandée

Durée : 45 à 60 minutes.

Objectif : avancer sur une room sans chercher à tout finir trop vite.

Méthode :
1. Lire les consignes en anglais.
2. Noter les mots techniques inconnus.
3. Répondre aux questions.
4. Faire un résumé en français dans Notes.
5. Ajouter les compétences vues dans ControlHub AI.
"""


def generate_linux_session():
    return """### Session Linux recommandée

Objectif : reprendre le lab Ubuntu / Apache.

Plan :

    sudo apt update
    sudo apt install apache2
    systemctl status apache2
    ss -tuln
    hostname -I

À la fin, note ce qui fonctionne et ce qui bloque encore.
"""


def generate_checklist():
    return """### Checklist générée

- [ ] Définir l’objectif de la session
- [ ] Ouvrir les bons outils
- [ ] Travailler 45 à 90 minutes
- [ ] Noter les résultats
- [ ] Faire un commit si nécessaire
- [ ] Préparer la prochaine action
"""


def run_agent_action(action, profile, skills, projects, goals):
    priority_goal = get_priority_goal(goals)

    if action == "Préparer ma journée":
        return generate_day_plan(priority_goal)

    if action == "Générer une tâche prioritaire":
        return generate_priority_task(priority_goal)

    if action == "Résumer ma progression":
        return generate_progress_summary(profile, skills, projects, goals)

    if action == "Préparer un post LinkedIn":
        return generate_linkedin_post()

    if action == "Préparer un email de relance":
        return generate_followup_email()

    if action == "Proposer une amélioration GitHub":
        return generate_github_improvements()

    if action == "Préparer une session TryHackMe":
        return generate_tryhackme_session()

    if action == "Préparer une session Linux":
        return generate_linux_session()

    if action == "Créer une checklist":
        return generate_checklist()

    return "Action non reconnue."