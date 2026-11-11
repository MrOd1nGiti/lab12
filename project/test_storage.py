from pathlib import Path
from tempfile import TemporaryDirectory
from storage import load_records, save_records


def test_storage_operations():
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "data.json"

        # Загрузка отсутствующего файла
        recs, msg = load_records(path)
        assert recs == []

        # Сохранение
        test_data = [{"id": 1, "title": "Task", "category": "Cat", "amount": 2, "completed": False}]
        success, _ = save_records(path, test_data)
        assert success is True

        # Повторная загрузка
        recs_loaded, msg = load_records(path)
        assert recs_loaded == test_data


if __name__ == "__main__":
    test_storage_operations()
    print("Все тесты хранилища успешно пройдены")
