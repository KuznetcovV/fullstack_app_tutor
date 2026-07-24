from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lesson_log import LessonLog


async def seed_lesson_logs(db: AsyncSession):
    
    result = await db.execute(select(LessonLog).limit(1))
    exists =result.scalar_one_or_none()
    if exists:
        print("Lesson logs already exists")
        return

    lesson_logs = [
        # ==========================
        # Иван Петров (student_id=1)
        # lesson_id=1 (Пн)
        # lesson_id=5 (Ср)
        # lesson_id=7 (Пт)
        # ==========================

        LessonLog(
            student_id=1,
            lesson_id=1,
            lesson_log_date=date(2025, 9, 1),   # Понедельник
            topic="Линейные уравнения",
            textbook="Алгебра 9",
            solved_tasks="№15-22",
            grade=5,
            comment="Отлично"
        ),

        LessonLog(
            student_id=1,
            lesson_id=5,
            lesson_log_date=date(2025, 9, 3),   # Среда
            topic="Квадратные уравнения",
            textbook="Алгебра 9",
            solved_tasks="№101-110",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=1,
            lesson_id=7,
            lesson_log_date=date(2025, 9, 5),   # Пятница
            topic="Функции",
            textbook="Алгебра 9",
            solved_tasks="№201-210",
            grade=4,
            comment="Ошибки в графиках"
        ),

        LessonLog(
            student_id=1,
            lesson_id=1,
            lesson_log_date=date(2025, 9, 8),
            topic="Неравенства",
            textbook="Алгебра 9",
            solved_tasks="№40-48",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=1,
            lesson_id=5,
            lesson_log_date=date(2025, 9, 10),
            topic="Системы уравнений",
            textbook="Алгебра 9",
            solved_tasks="№301-309",
            grade=5,
            comment="Быстро усваивает материал"
        ),

        # ==========================
        # Мария Сидорова (student_id=2)
        # lesson_id=2 (Пн)
        # lesson_id=8 (Пт)
        # ==========================

        LessonLog(
            student_id=2,
            lesson_id=2,
            lesson_log_date=date(2025, 9, 1),
            topic="Производная",
            textbook="Алгебра 10",
            solved_tasks="№11-18",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=2,
            lesson_id=8,
            lesson_log_date=date(2025, 9, 5),
            topic="Исследование функций",
            textbook="Алгебра 10",
            solved_tasks="№55-63",
            grade=5,
            comment="Все решила самостоятельно"
        ),

        LessonLog(
            student_id=2,
            lesson_id=2,
            lesson_log_date=date(2025, 9, 8),
            topic="Экстремумы",
            textbook="Алгебра 10",
            solved_tasks="№70-78",
            grade=4,
            comment="Небольшие ошибки"
        ),

        LessonLog(
            student_id=2,
            lesson_id=8,
            lesson_log_date=date(2025, 9, 12),
            topic="Первообразная",
            textbook="Алгебра 10",
            solved_tasks="№100-109",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=2,
            lesson_id=2,
            lesson_log_date=date(2025, 9, 15),
            topic="Интеграл",
            textbook="Алгебра 10",
            solved_tasks="№120-128",
            grade=5,
            comment="Очень хороший прогресс"
        ),

        # ==========================
        # Дмитрий Иванов (student_id=3)
        # lesson_id=3 (Пн)
        # lesson_id=9 (Пт)
        # ==========================

        LessonLog(
            student_id=3,
            lesson_id=3,
            lesson_log_date=date(2025, 9, 1),
            topic="Тригонометрия",
            textbook="Алгебра 11",
            solved_tasks="№1-10",
            grade=3,
            comment="Много пробелов"
        ),

        LessonLog(
            student_id=3,
            lesson_id=9,
            lesson_log_date=date(2025, 9, 5),
            topic="Формулы приведения",
            textbook="Алгебра 11",
            solved_tasks="№20-28",
            grade=4,
            comment=None
        ),

        LessonLog(
            student_id=3,
            lesson_id=3,
            lesson_log_date=date(2025, 9, 8),
            topic="Логарифмы",
            textbook="Алгебра 11",
            solved_tasks="№45-53",
            grade=4,
            comment="Есть прогресс"
        ),

        LessonLog(
            student_id=3,
            lesson_id=9,
            lesson_log_date=date(2025, 9, 12),
            topic="Показательные уравнения",
            textbook="Алгебра 11",
            solved_tasks="№70-79",
            grade=5,
            comment="Домашняя работа выполнена"
        ),

        LessonLog(
            student_id=3,
            lesson_id=3,
            lesson_log_date=date(2025, 9, 15),
            topic="Подготовка к ЕГЭ",
            textbook="ЕГЭ профиль",
            solved_tasks="Вариант №3",
            grade=4,
            comment=None
        ),

        # ==========================
        # Антон Харчук (student_id=4)
        # lesson_id=4 (Вт)
        # lesson_id=6 (Чт)
        # ==========================

        LessonLog(
            student_id=4,
            lesson_id=4,
            lesson_log_date=date(2025, 9, 2),   # Вторник
            topic="Обыкновенные дроби",
            textbook="Математика 8",
            solved_tasks="№12-20",
            grade=3,
            comment="Домашнее задание не сделал"
        ),

        LessonLog(
            student_id=4,
            lesson_id=6,
            lesson_log_date=date(2025, 9, 4),   # Четверг
            topic="Десятичные дроби",
            textbook="Математика 8",
            solved_tasks="№30-39",
            grade=4,
            comment=None
        ),

        LessonLog(
            student_id=4,
            lesson_id=4,
            lesson_log_date=date(2025, 9, 9),
            topic="Пропорции",
            textbook="Математика 8",
            solved_tasks="№45-55",
            grade=4,
            comment="Начал работать активнее"
        ),

        LessonLog(
            student_id=4,
            lesson_id=6,
            lesson_log_date=date(2025, 9, 11),
            topic="Линейные функции",
            textbook="Алгебра 8",
            solved_tasks="№70-80",
            grade=5,
            comment="Молодец"
        ),

        LessonLog(
            student_id=4,
            lesson_id=4,
            lesson_log_date=date(2025, 9, 16),
            topic="Контрольная работа",
            textbook=None,
            solved_tasks="Вариант 2",
            grade=4,
            comment="Ошибки по невнимательности"
        ),

        LessonLog(
            student_id=5,
            lesson_id=10,
            lesson_log_date=date(2026, 1, 5),
            topic="Линейные уравнения",
            textbook="Алгебра 9",
            solved_tasks="№120-130",
            grade=5,
            comment="Отличная работа"
        ),

        LessonLog(
            student_id=5,
            lesson_id=11,
            lesson_log_date=date(2026, 1, 6),
            topic="Квадратные уравнения",
            textbook="Алгебра 9",
            solved_tasks="№210-220",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=5,
            lesson_id=10,
            lesson_log_date=date(2026, 1, 12),
            topic="Теорема Виета",
            textbook="Алгебра 9",
            solved_tasks="№230-235",
            grade=4,
            comment=None
        ),

        LessonLog(
            student_id=5,
            lesson_id=11,
            lesson_log_date=date(2026, 1, 13),
            topic="Функции",
            textbook="Алгебра 9",
            solved_tasks="№310-315",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=5,
            lesson_id=10,
            lesson_log_date=date(2026, 1, 19),
            topic="Контрольная",
            textbook=None,
            solved_tasks=None,
            grade=5,
            comment="Все отлично"
        ),

        LessonLog(
            student_id=6,
            lesson_id=13,
            lesson_log_date=date(2026,1,6),
            topic="Производная",
            textbook="Профиль",
            solved_tasks="№1-8",
            grade=4,
            comment=None
        ),

        LessonLog(
            student_id=6,
            lesson_id=12,
            lesson_log_date=date(2026,1,7),
            topic="Исследование функций",
            textbook="Профиль",
            solved_tasks="№9-18",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=6,
            lesson_id=13,
            lesson_log_date=date(2026,1,13),
            topic="Логарифмы",
            textbook="Профиль",
            solved_tasks="№30-38",
            grade=4,
            comment=None
        ),

        LessonLog(
            student_id=6,
            lesson_id=12,
            lesson_log_date=date(2026,1,14),
            topic="Пределы",
            textbook="Профиль",
            solved_tasks="№40-47",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=6,
            lesson_id=12,
            lesson_log_date=date(2026,1,21),
            topic="ЕГЭ вариант",
            textbook=None,
            solved_tasks=None,
            grade=5,
            comment="Очень сильное занятие"
        ),

        LessonLog(
            student_id=7,
            lesson_id=14,
            lesson_log_date=date(2026,1,8),
            topic="Дроби",
            textbook="Математика 7",
            solved_tasks="№45-58",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=7,
            lesson_id=15,
            lesson_log_date=date(2026,1,15),
            topic="Пропорции",
            textbook="Математика 7",
            solved_tasks="№70-82",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=7,
            lesson_id=14,
            lesson_log_date=date(2026,1,22),
            topic="Проценты",
            textbook="Математика 7",
            solved_tasks="№91-103",
            grade=4,
            comment=None
        ),

        LessonLog(
            student_id=7,
            lesson_id=15,
            lesson_log_date=date(2026,1,29),
            topic="Уравнения",
            textbook="Математика 7",
            solved_tasks="№120-130",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=7,
            lesson_id=14,
            lesson_log_date=date(2026,2,5),
            topic="Контрольная",
            textbook=None,
            solved_tasks=None,
            grade=5,
            comment="Заметный прогресс"
        ),

        LessonLog(
            student_id=8,
            lesson_id=17,
            lesson_log_date=date(2026,1,7),
            topic="Степени",
            textbook="Алгебра 10",
            solved_tasks="№15-28",
            grade=3,
            comment="Нужно повторить"
        ),

        LessonLog(
            student_id=8,
            lesson_id=16,
            lesson_log_date=date(2026,1,9),
            topic="Корни",
            textbook="Алгебра 10",
            solved_tasks="№35-47",
            grade=4,
            comment=None
        ),

        LessonLog(
            student_id=8,
            lesson_id=17,
            lesson_log_date=date(2026,1,14),
            topic="Логарифмы",
            textbook="Алгебра 10",
            solved_tasks="№60-70",
            grade=4,
            comment=None
        ),

        LessonLog(
            student_id=8,
            lesson_id=16,
            lesson_log_date=date(2026,1,16),
            topic="Показательные функции",
            textbook="Алгебра 10",
            solved_tasks="№80-95",
            grade=5,
            comment=None
        ),

        LessonLog(
            student_id=8,
            lesson_id=17,
            lesson_log_date=date(2026,1,21),
            topic="Повторение",
            textbook=None,
            solved_tasks=None,
            grade=4,
            comment="Стал увереннее"
        ),
    ]

    db.add_all(lesson_logs)
    await db.commit()

    print("Lesson logs seeded")