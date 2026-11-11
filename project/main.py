from pathlib import Path
from logic import add_record, delete_record, find_records, set_completed, statistics
from storage import load_records, save_records


def read_positive_integer(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
        except ValueError:
            print("Ошибка: введите целое число")
            continue
        if val < 0:
            print("Ошибка: число не может быть отрицательным")
            continue
        return val


def main():
    folder = Path(__file__).resolve().parent
    data_path = folder / "data.json"

    records, message = load_records(data_path)
    print(message)
    if records is None:
        print("Запуск прерван из-за ошибки в файле данных")
        return

    while True:
        print("\n--- ПЛАН УЧЕБНЫХ ЗАНЯТИЙ ---")
        print("1. Показать записи")
        print("2. Добавить запись")
        print("3. Найти записи")
        print("4. Изменить статус")
        print("5. Удалить запись")
        print("6. Показать статистику")
        print("7. Сохранить данные")
        print("8. Выйти")

        choice = input("Выберите пункт меню (1-8): ").strip()

        if choice == "1":
            if not records:
                print("Нет записей")
            else:
                for r in sorted(records, key=lambda x: x["id"]):
                    status = "Выполнено" if r["completed"] else "Не выполнено"
                    print(f"ID: {r['id']} | Название: {r['title']} | Категория: {r['category']} | Часы: {r['amount']} | Статус: {status}")

        elif choice == "2":
            title = input("Введите название занятия: ")
            category = input("Введите категорию: ")
            amount = read_positive_integer("Введите количество часов: ")
            try:
                new_id = add_record(records, title, category, amount)
                print(f"Запись успешно добавлена с ID {new_id}")
            except ValueError as error:
                print(f"Ошибка: {error}")

        elif choice == "3":
            query = input("Введите поисковый запрос (подстрока названия): ")
            try:
                found = find_records(records, query)
                if not found:
                    print("Ничего не найдено")
                else:
                    print(f"Найдено записей: {len(found)}")
                    for r in found:
                        status = "Выполнено" if r["completed"] else "Не выполнено"
                        print(f"ID: {r['id']} | Название: {r['title']} | Категория: {r['category']} | Часы: {r['amount']} | Статус: {status}")
            except ValueError as error:
                print(f"Ошибка: {error}")

        elif choice == "4":
            rec_id = read_positive_integer("Введите ID записи: ")
            status_input = input("Установить статус выполненным? (да/нет): ").strip().lower()
            if status_input == "да":
                completed_val = True
            elif status_input == "нет":
                completed_val = False
            else:
                print("Неверный ответ, отмена операции")
                continue

            if set_completed(records, rec_id, completed_val):
                print("Статус успешно изменён")
            else:
                print("Запись с таким ID не найдена")

        elif choice == "5":
            rec_id = read_positive_integer("Введите ID записи для удаления: ")
            confirm = input(f"Вы действительно хотите удалить запись с ID {rec_id}? (да/нет): ").strip().lower()
            if confirm == "да":
                if delete_record(records, rec_id):
                    print("Запись удалена")
                else:
                    print("Запись с таким ID не найдена")
            else:
                print("Удаление отменено")

        elif choice == "6":
            stats = statistics(records)
            print(f"Общее количество записей: {stats['total_count']}")
            print(f"Выполнено: {stats['completed_count']}")
            print(f"Не выполнено: {stats['uncompleted_count']}")
            print(f"Сумма часов (всего): {stats['total_amount']}")
            print("Суммы по категориям:")
            if not stats["categories"]:
                print("  Нет категорий")
            else:
                for cat, amt in stats["categories"].items():
                    print(f"  {cat} - {amt} часов")

        elif choice == "7":
            success, msg = save_records(data_path, records)
            print(msg)

        elif choice == "8":
            while True:
                save_prompt = input("Сохранить текущие данные перед выходом? (да/нет): ").strip().lower()
                if save_prompt == "да":
                    success, msg = save_records(data_path, records)
                    print(msg)
                    if success:
                        return
                    break
                elif save_prompt == "нет":
                    return
                else:
                    print("Пожалуйста, ответьте 'да' или 'нет'")

        else:
            print("Неверный выбор. Введите число от 1 до 8.")


if __name__ == "__main__":
    main()
