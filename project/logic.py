def validate_records(records):
    if not isinstance(records, list):
        raise ValueError("Корень JSON должен быть списком")

    seen_ids = set()
    for index, item in enumerate(records):
        if not isinstance(item, dict):
            raise ValueError(f"Элемент с индексом {index} не является словарём")

        required_keys = {"id", "title", "category", "amount", "completed"}
        if not required_keys.issubset(item.keys()):
            raise ValueError(f"Элемент с индексом {index}: отсутствуют обязательные поля")

        if type(item["id"]) is not int or item["id"] <= 0:
            raise ValueError(f"Элемент с индексом {index}: 'id' должно быть положительным целым числом")

        record_id = item["id"]
        if record_id in seen_ids:
            raise ValueError(f"Обнаружен дубликат id: {record_id}")
        seen_ids.add(record_id)

        if type(item["title"]) is not str or not item["title"].strip():
            raise ValueError(f"Элемент с индексом {index}: 'title' должно быть непустой строкой")

        if type(item["category"]) is not str or not item["category"].strip():
            raise ValueError(f"Элемент с индексом {index}: 'category' должно быть непустой строкой")

        if type(item["amount"]) is not int or isinstance(item["amount"], bool) or item["amount"] < 0:
            raise ValueError(f"Элемент с индексом {index}: 'amount' должно быть целым неотрицательным числом")

        if type(item["completed"]) is not bool:
            raise ValueError(f"Элемент с индексом {index}: 'completed' должно быть логического типа")


def add_record(records, title, category, amount):
    clean_title = title.strip()
    clean_category = category.strip()

    if not clean_title:
        raise ValueError("Название не должно быть пустым")
    if not clean_category:
        raise ValueError("Категория не должна быть пустой")
    if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
        raise ValueError("Количество часов должно быть целым неотрицательным числом")

    max_id = 0
    for record in records:
        if record["id"] > max_id:
            max_id = record["id"]
    new_id = max_id + 1

    new_record = {
        "id": new_id,
        "title": clean_title,
        "category": clean_category,
        "amount": amount,
        "completed": False,
    }
    records.append(new_record)
    return new_id


def find_records(records, query):
    clean_query = query.strip().lower()
    if not clean_query:
        return []

    found = []
    for record in records:
        if clean_query in record["title"].lower():
            found.append(record)
    return found


def set_completed(records, record_id, completed):
    for record in records:
        if record["id"] == record_id:
            record["completed"] = completed
            return True
    return False


def delete_record(records, record_id):
    for index, record in enumerate(records):
        if record["id"] == record_id:
            records.pop(index)
            return True
    return False


def statistics(records):
    total_count = len(records)
    completed_count = 0
    uncompleted_count = 0
    total_amount = 0
    categories_amount = {}

    for record in records:
        total_amount += record["amount"]
        if record["completed"]:
            completed_count += 1
        else:
            uncompleted_count += 1

        cat = record["category"].strip()
        if cat not in categories_amount:
            categories_amount[cat] = 0
        categories_amount[cat] += record["amount"]

    sorted_categories = {}
    for cat in sorted(categories_amount.keys()):
        sorted_categories[cat] = categories_amount[cat]

    return {
        "total_count": total_count,
        "completed_count": completed_count,
        "uncompleted_count": uncompleted_count,
        "total_amount": total_amount,
        "categories": sorted_categories,
    }
