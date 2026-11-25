import json, os
from models import Patient

data_file = os.path.join(os.path.dirname(__file__), "data.json")

def load_patients(path: str = data_file) -> list[Patient]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    patients = []
    for item in raw:
        item.pop("bmi", None)
        try:
            patients.append(Patient(**item))
        except (ValueError, TypeError) as e:
            print(f"строка обязательнa {item}: {e} для заполнения")
    return patients

def save_patients(patients: list[Patient], path: str = data_file) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in patients], f, ensure_ascii=False, indent=2)