# alembic downgrade -1
# alembic upgrade head
# alembic revision --autogenerate -m "описание миграции"
# docker compose up
# CREATE TYPE userroleenum AS ENUM ('admin', 'user', 'super_user');

# UPDATE users
# SET user_role = 'super_user'
# WHERE id = 1;
