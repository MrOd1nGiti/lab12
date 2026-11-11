import json
from pathlib import Path


def load_records(path):
    path = Path(path)
    if not path.exists():
        return [], "Файл не найден, начат новый список"

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except UnicodeError:
        return None, "Ошибка: неверная кодировка файла (ожидается UTF-8)"
    except json.JSONDecodeError as error:
        return None, f"Ошибка синтаксиса JSON: {error}"
    except OSError as error:
        return None, f"Ошибка файлового доступа: {error}"

    try:
        from logic import validate_records
        validate_records(data)
    except ValueError as error:
        return None, f"Ошибка структуры данных: {error}"

    return data, "Данные успешно загружены"


def save_records(path, records):
    path = Path(path)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=2)
        return True, "Данные успешно сохранены"
    except OSError as error:
        return False, f"Ошибка при сохранении файла: {error}"
