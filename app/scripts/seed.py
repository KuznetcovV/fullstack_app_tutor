import asyncio

from app.core.database import AsyncSessionLocal
from app.scripts.seeds.students import seed_students
from app.scripts.seeds.lessons import seed_lessons
from app.scripts.seeds.subscriptions import seed_subscriptions
from app.scripts.seeds.lesson_logs import seed_lesson_logs


async def main():
    async with AsyncSessionLocal() as session:
        await seed_students(session)
        await seed_lessons(session)
        await seed_subscriptions(session)
        await seed_lesson_logs(session)


if __name__ == "__main__":
    asyncio.run(main())