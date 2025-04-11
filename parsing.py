import xlrd
import re
from typing import List, Dict

def parse_schedule(file_path: str, target_group: str = None) -> List[Dict]:
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_name("Лист1")

    schedule = []
    current_day = None
    group_columns = {"2991": 2, "2992": 5}
    time_slots = {}

    for row_idx in range(6, sheet.nrows):
        row = sheet.row_values(row_idx)
        day_candidate = str(row[0]).strip().capitalize()
        if day_candidate in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]:
            current_day = day_candidate
            time_slots = {}
            continue

        raw_time = str(row[1]).strip()
        if not current_day or not raw_time or ":" in raw_time:
            continue

        normalized_time = raw_time.replace(".", ":")
        start_time = normalized_time.split("-")[0]
        pair_type = determine_pair_type(current_day, start_time, time_slots)

        for group, col in group_columns.items():
            if target_group and group != target_group:
                continue

            # Разделяем ячейку на верхнюю и нижнюю неделю, если есть разделитель
            cell_value = str(row[col]).strip()
            if cell_value and "\n" in cell_value:
                top_week_value, bottom_week_value = cell_value.split("\n")
                process_lessons(schedule, current_day, normalized_time, pair_type + " (верхняя)", group, top_week_value)
                process_lessons(schedule, current_day, normalized_time, pair_type + " (нижняя)", group, bottom_week_value)
            else:
                process_lessons(schedule, current_day, normalized_time, pair_type, group, cell_value)

    return schedule

def determine_pair_type(current_day: str, start_time: str, time_slots: Dict) -> str:
    """Определяет тип пары ("Верхняя" или "Нижняя") на основе времени."""
    if current_day not in time_slots:
        time_slots[current_day] = []
    if start_time not in time_slots[current_day]:
        time_slots[current_day].append(start_time)
    pair_index = time_slots[current_day].index(start_time)
    return "Верхняя" if pair_index % 2 == 0 else "Нижняя"

def process_lessons(schedule: List[Dict], current_day: str, normalized_time: str, pair_type: str, group: str, lesson_data: str):
    """Обрабатывает данные об уроке и добавляет их в расписание."""
    if not lesson_data or lesson_data == "-":
        return

    lessons = split_lessons(lesson_data)
    for lesson in lessons:
        schedule.append({
            "day": current_day,
            "time": normalized_time,
            "type": f"{pair_type} пара",
            "group": group,
            **lesson
        })

def split_lessons(text: str) -> List[Dict]:
    lessons = []
    elements = [e.strip() for e in re.split(r",\s*", text) if e]

    i = 0
    while i < len(elements):
        lesson = {"subject": "", "other": ""}

        # Проверяем, есть ли хотя бы название предмета
        if i < len(elements):
            lesson["subject"] = elements[i]
            # Собираем "остальное"
            remaining_elements = elements[i+1:min(i+4, len(elements))]
            lesson["other"] = ", ".join(remaining_elements)
            lessons.append(lesson)
            i += 4
        else:
            break

    return lessons

def print_schedule(schedule: List[Dict]) -> None:
    for entry in schedule:
        print(f"День: {entry['day']}")
        print(f"Время: {entry['time']}")
        print(f"Тип: {entry['type']}")
        print(f"Группа: {entry['group']}")
        print(f"Название предмета: {entry['subject']}")
        print(f"Остальное: {entry['other']}")
        print("-" * 30)

if __name__ == "__main__":
    schedule = parse_schedule("2991_2992.xls", target_group="2992")
    print_schedule(schedule)
