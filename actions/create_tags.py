import asyncio
from typing import Dict

from app.core.models import db_helper
from app.core.models.tag import TagAlchemyModel

default_colors = {
    "Красный": "#FF0000",
    "Зелёный": "#00FF00",
    "Синий": "#0000FF",
    "Чёрный": "#000000",
    "Белый": "#FFFFFF",
    "Жёлтый": "#FFFF00",
    "Голубой": "#00FFFF",
    "Розовый": "#FFC0CB",
    "Бирюзовый": "#40E0D0",
    "Оранжевый": "#FFA500",
    "Фиолетовый": "#800080",
    "Коричневый": "#A52A2A",
}


async def create_tags(
    colors: Dict[str, str] = default_colors,
):
    tags = [
        TagAlchemyModel(
            tag_name=color,
            tag_color=colors[color],
        )
        for color in colors
    ]

    return tags


async def create():
    async with db_helper.session_factory() as session:
        tags = await create_tags()
        session.add_all(tags)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(create())
