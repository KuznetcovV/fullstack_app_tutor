from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student

async def seed_students(db: AsyncSession):

    result = await db.execute(select(Student).limit(1))
    exists = result.scalar_one_or_none()
    if exists:
        print("Students already exists")
        return

    students = [
        Student(
            first_name="Иван",
            last_name="Петров",
            number_of_class=9,
            phone="+79969133520",
            parent_name="Алексей Петров",
            parent_phone="89992223344",
            notes="Хорошо понимает дроби",
            is_active=True
        ),

        Student(
            first_name="Мария",
            last_name="Сидорова",
            number_of_class=10,
            phone="89912312312",
            parent_name="Елена Сидорова",
            parent_phone="89992223344",
            notes=None,
            is_active=True
        ),

        Student(
            first_name="Дмитрий",
            last_name="Иванов",
            number_of_class=11,
            phone=None,
            parent_name=None,
            parent_phone=None,
            notes="Подготовка к ЕГЭ",
            is_active=False
        ),

        Student(
            first_name="Антон",
            last_name="Харчук",
            number_of_class=8,
            phone="+79969133521",
            parent_name=None,
            parent_phone=None,
            notes="Не выполняет дз",
            is_active=True
        ),

        Student(
            first_name="Екатерина",
            last_name="Орлова",
            number_of_class=9,
            phone="+79961111111",
            parent_name="Ольга Орлова",
            parent_phone="+79962222222",
            notes="Любит геометрию",
            is_active=True
        ),

        Student(
            first_name="Максим",
            last_name="Козлов",
            number_of_class=11,
            phone="+79963333333",
            parent_name="Игорь Козлов",
            parent_phone="+79964444444",
            notes="Подготовка к профильной математике",
            is_active=True
        ),

        Student(
            first_name="Алина",
            last_name="Морозова",
            number_of_class=7,
            phone=None,
            parent_name="Наталья Морозова",
            parent_phone="+79965555555",
            notes=None,
            is_active=True
        ),

        Student(
            first_name="Кирилл",
            last_name="Васильев",
            number_of_class=10,
            phone="+79966666666",
            parent_name="Сергей Васильев",
            parent_phone="+79967777777",
            notes="Часто пропускает",
            is_active=True
        ),

    ]

    db.add_all(students)

    await db.commit()

    print("Students seeded")