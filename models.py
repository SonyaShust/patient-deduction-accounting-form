import re
from dataclasses import dataclass, field, asdict

name_re= re.compile(r"^[А-Яа-яЁё\- ]+$")

def validate_name(value: str, field_name: str = "поле") -> str:
    """Проверяет, что в строке только буквы и дефисы, без цифр/символов."""
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name}: Это поле обязательно для заполнения")
    if any(ch.isdigit() for ch in value):
        raise ValueError(f"{field_name}: цифры недопустимы")
    if not name_re.match(value):
        raise ValueError(f"{field_name}: допустимы только буквы и дефис")
    return value


@dataclass
class Patient:
    last_name: str      
    first_name: str    
    middle_name: str   
    age: int
    gender: str
    height: float       
    weight: float       

    def __post_init__(self):
        self.last_name = validate_name(self.last_name, "Фамилия")
        self.first_name = validate_name(self.first_name, "Имя")
        if self.middle_name:
            self.middle_name = validate_name(self.middle_name, "Отчество")
        if not (1 <= self.age <= 2931):
            raise ValueError("Возраст должен быть от 1 до 2931")
        if self.gender not in ("М", "Ж","Не определен"):
            raise ValueError("Пол должен быть 'М','Ж' или  'Не определен' ")
        if not (0.1 <= self.height <= 300):
            raise ValueError("Рост должен быть от 0.1 до 300 см")
        if not (0.1 <= self.weight <= 700):
            raise ValueError("Вес должен быть от 0.1 до 700 кг")

    @property
    def bmi(self) -> float:
        """ИМТ = вес(кг) / рост(м)^2. Вычисляется автоматически."""
        h_m = self.height / 100
        return round(self.weight / (h_m ** 2), 1)

    @property
    def fio(self) -> str:
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(p for p in parts if p)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["bmi"] = self.bmi
        return d