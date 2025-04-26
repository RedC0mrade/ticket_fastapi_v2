# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.factories.database import db_helper
# from app.validators.ticket_tag_association import AssociationValidation


# def get_association_validation(
#     session: AsyncSession = Depends(db_helper.session_getter),
# ) -> AssociationValidation:
#     return AssociationValidation(session=session)
