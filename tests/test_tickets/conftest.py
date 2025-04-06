import pytest
import tests

@pytest.fixture(scope="function")
async def first_user_ticket_to_second(first_user, tag_white, tag_black, session,):
    pass