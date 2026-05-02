import streamlit as st


def render_roadmap_page():
    st.title("🧭 Roadmap")

    st.write(
        "Cette roadmap sert à structurer ta progression vers le BTS SIO SISR, "
        "les systèmes, réseaux, cybersécurité et l’automatisation avec Python/IA."
    )

    roadmap = [
        {
            "phase": "Phase 1 — Fondations",
            "status": "en cours",
            "tasks": [
                "Consolider Git/GitHub",
                "Continuer ControlHub AI",
                "Documenter les apprentissages dans le learning log",
                "Organiser les projets existants",
            ],
        },
        {
            "phase": "Phase 2 — Réseaux",
            "status": "en cours",
            "tasks": [
                "Améliorer les README des labs Cisco Packet Tracer",
                "Revoir IP, masque, passerelle, DNS, DHCP",
                "Revoir VLAN, routage inter-VLAN et NAT/PAT",
                "Ajouter un lab ACL si nécessaire",
            ],
        },
        {
            "phase": "Phase 3 — Linux / Systèmes",
            "status": "à reprendre",
            "tasks": [
                "Reprendre la VM Ubuntu",
                "Diagnostiquer Apache",
                "Comprendre systemctl, services, ports et pare-feu",
                "Créer un mini-projet GitHub Ubuntu Web Server Lab",
            ],
        },
        {
            "phase": "Phase 4 — Cybersécurité défensive",
            "status": "commencé",
            "tasks": [
                "Continuer TryHackMe",
                "Résumer chaque room importante",
                "Comprendre logs, détection, durcissement et bonnes pratiques",
                "Créer des notes cyber en français",
            ],
        },
        {
            "phase": "Phase 5 — Portfolio professionnel",
            "status": "en cours",
            "tasks": [
                "Rendre GitHub plus lisible",
                "Ajouter des descriptions propres aux projets",
                "Préparer des posts LinkedIn",
                "Préparer le pitch alternance BTS SIO SISR",
            ],
        },
        {
            "phase": "Phase 6 — IA / Automatisation",
            "status": "en construction",
            "tasks": [
                "Améliorer le dashboard ControlHub AI",
                "Ajouter une vraie génération de tâches",
                "Ajouter une page notes",
                "Connecter une IA plus tard",
            ],
        },
    ]

    for item in roadmap:
        with st.expander(f"{item['phase']} — {item['status']}"):
            for task in item["tasks"]:
                st.checkbox(task, value=False)

    st.divider()

    st.header("🔥 Prochaine action recommandée")

    st.success("Reprendre le lab Ubuntu Apache")
    st.write(
        "C’est une bonne priorité car elle relie Linux, réseau, services système, "
        "diagnostic et cybersécurité de base."
    )

    st.markdown("### Plan rapide")
    st.write("1. Démarrer la VM Ubuntu")
    st.write("2. Vérifier si Apache est installé")
    st.write("3. Vérifier le statut du service Apache")
    st.write("4. Vérifier le port 80")
    st.write("5. Tester dans le navigateur")
    st.write("6. Noter le résultat dans le learning log")