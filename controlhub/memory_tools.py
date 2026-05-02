from controlhub.storage import MEMORY_FILE, load_json, save_json


def load_memory():
    return load_json(MEMORY_FILE, [])


def add_memory_item(category, content, importance):
    memory = load_memory()

    memory.append(
        {
            "category": category.strip(),
            "content": content.strip(),
            "importance": importance.strip(),
        }
    )

    save_json(MEMORY_FILE, memory)


def format_memory_for_ai():
    memory = load_memory()

    if not memory:
        return "Aucune mémoire personnelle enregistrée."

    lines = ["Mémoire personnelle de l'utilisateur :"]

    high_importance = [
        item for item in memory if item.get("importance") == "haute"
    ]
    other_items = [
        item for item in memory if item.get("importance") != "haute"
    ]

    ordered_memory = high_importance + other_items

    for item in ordered_memory:
        category = item.get("category", "Non catégorisé")
        content = item.get("content", "")
        importance = item.get("importance", "moyenne")

        lines.append(f"- [{importance}] {category} : {content}")

    return "\n".join(lines)