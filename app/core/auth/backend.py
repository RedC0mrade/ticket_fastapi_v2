from fastapi_users.authentication import JWTStrategy, AuthenticationBackend

SECRET = "SUPER_SECRET_KEY"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=JWTStrategy(secret=SECRET, lifetime_seconds=3600),
    get_strategy=get_jwt_strategy,
)
