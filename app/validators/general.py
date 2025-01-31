from fastapi import HTTPException, status


def validate_actions_with_same_id(
    user_id: int,
    second_user_id: int,
):
    if second_user_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"user id specified id = {user_id}",
        )
