# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends

# from app.factories.database import db_helper
# from app.validators.user import UserValidation


# def get_validation_user(
#     session: AsyncSession = Depends(db_helper.session_getter),
# ) -> UserValidation:
#     """Фабрика для получения экземпляра валидатора пользователя"""
#     return UserValidation(session)
