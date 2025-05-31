import json
from .utils import resource_path

def load_regulations():
    json_path = resource_path("assets/regulations.json")
    with open(json_path, "r") as f:
        return json.load(f)


def format_regulations(species, regulations):
    reg = regulations.get(species)
    if not reg:
        return "No regulations found."

    text = f"Regulations for {species}\n\n"
    for key, value in reg.items():
        text += f"{key}:\n"
        if isinstance(value, dict):
            for region, val in value.items():
                text += f"  - {region}: {val}\n"
        elif isinstance(value, list):
            for item in value:
                text += f"  - {item}\n"
        else:
            text += f"  - {value}\n"
        text += "\n"
    return text.strip()
