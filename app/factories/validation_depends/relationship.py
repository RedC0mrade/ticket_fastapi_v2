# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.factories.database import db_helper
# from app.validators.relationship import RelationshipValidation


# def get_relationship_validation(
#     session: AsyncSession = Depends(db_helper.session_getter),
# ) -> RelationshipValidation:
#     return RelationshipValidation(
#         session=session,
#     )
