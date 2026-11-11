from logic import add_record, delete_record, find_records, set_completed, statistics, validate_records


def test_validate_records():
    valid = [{"id": 1, "title": "A", "category": "б", "amount": 3, "completed": True}]
    validate_records(valid)

    try:
        validate_records("not a list")
        assert False
    except ValueError:
        pass


def test_add_and_delete():
    records = []
    id1 = add_record(records, "  Тест  ", " Проекты ", 5)
    assert id1 == 1
    assert records[0]["title"] == "Тест"
    assert records[0]["category"] == "Проекты"
    assert records[0]["amount"] == 5
    assert records[0]["completed"] is False

    assert delete_record(records, 999) is False
    assert delete_record(records, 1) is True
    assert len(records) == 0


def test_find_and_stats():
    records = [
        {"id": 1, "title": "Python Basics", "category": "IT", "amount": 10, "completed": True},
        {"id": 2, "title": "Python Advanced", "category": "IT", "amount": 5, "completed": False},
        {"id": 3, "title": "English Grammar", "category": "Языки", "amount": 4, "completed": True}
    ]

    found = find_records(records, "python")
    assert len(found) == 2

    assert find_records(records, "   ") == []

    assert set_completed(records, 2, True) is True
    assert records[1]["completed"] is True

    stats = statistics(records)
    assert stats["total_count"] == 3
    assert stats["completed_count"] == 3
    assert stats["uncompleted_count"] == 0
    assert stats["total_amount"] == 19
    assert stats["categories"]["IT"] == 15
    assert stats["categories"]["Языки"] == 4


if __name__ == "__main__":
    test_validate_records()
    test_add_and_delete()
    test_find_and_stats()
    print("Все тесты логики успешно пройдены")
