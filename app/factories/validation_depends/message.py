# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends

# from app.api.dependencies.current_users_depends import current_active_user
# from app.core.auth.schemas import UserRead
# from app.factories.database import db_helper
# from app.validators.message import MessageValidate


# def get_message_validation(
#     # session: AsyncSession = Depends(db_helper.session_getter),
#     user: UserRead = Depends(current_active_user),
# ):
#     return MessageValidate(
#         # session=session,
#         user=user,
#     )
