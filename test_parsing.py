import pytest
import xlrd
from parsing import parse_schedule, determine_pair_type, process_lessons, split_lessons


def test_parse_schedule():
    schedule = parse_schedule("2991_2992.xls")
    assert isinstance(schedule, list)
    assert all(isinstance(item, dict) for item in schedule)

def test_parse_schedule_with_target_group():
    schedule = parse_schedule("2991_2992.xls", target_group="2992")
    assert isinstance(schedule, list)
    assert all(isinstance(item, dict) for item in schedule)

def test_determine_pair_type():
    time_slots = {}
    pair_type = determine_pair_type("Понедельник", "09:00", time_slots)
    assert pair_type == "Верхняя"
    
    time_slots["Понедельник"] = ["09:00"]
    pair_type = determine_pair_type("Понедельник", "10:00", time_slots)
    assert pair_type == "Нижняя"

def test_process_lessons():
    schedule = []
    process_lessons(schedule, "Понедельник", "09:00", "Верхняя пара", "2992", "Математика, учитель Иванов")
    assert len(schedule) == 1
    assert schedule[0]["day"] == "Понедельник"
    assert schedule[0]["time"] == "09:00"
    assert schedule[0]["type"] == "Верхняя пара"
    assert schedule[0]["group"] == "2992"
    assert schedule[0]["subject"] == "Математика"
    assert schedule[0]["other"] == "учитель Иванов"

def test_split_lessons():
    lessons = split_lessons("Математика, учитель Иванов, кабинет 101")
    assert len(lessons) == 1
    assert lessons[0]["subject"] == "Математика"
    assert lessons[0]["other"] == "учитель Иванов, кабинет 101"

def test_split_lessons_multiple():
    lessons = split_lessons("Математика, учитель Иванов, кабинет 101, Физика, учитель Петров, кабинет 202")
    assert len(lessons) == 2
    assert lessons[0]["subject"] == "Математика"
    assert lessons[0]["other"] == "учитель Иванов, кабинет 101"
    assert lessons[1]["subject"] == "Физика"
    assert lessons[1]["other"] == "учитель Петров, кабинет 202"

# Тест на случай, когда в ячейке пустая строка или "-"
def test_process_lessons_empty():
    schedule = []
    process_lessons(schedule, "Понедельник", "09:00", "Верхняя пара", "2992", "")
    assert len(schedule) == 0

    process_lessons(schedule, "Понедельник", "09:00", "Верхняя пара", "2992", "-")
    assert len(schedule) == 0

# Тест на случай, когда в ячейке несколько предметов
def test_process_lessons_multiple_lessons():
    schedule = []
    lesson_data = "Математика, учитель Иванов\nФизика, учитель Петров"
    process_lessons(schedule, "Понедельник", "09:00", "Верхняя пара", "2992", lesson_data)
    assert len(schedule) == 2
    assert schedule[0]["day"] == "Понедельник"
    assert schedule[0]["time"] == "09:00"
    assert schedule[0]["type"] == "Верхняя пара"
    assert schedule[0]["group"] == "2992"
    assert schedule[0]["subject"] == "Математика"
    assert schedule[0]["other"] == "учитель Иванов"
    assert schedule[1]["subject"] == "Физика"
    assert schedule[1]["other"] == "учитель Петров"
