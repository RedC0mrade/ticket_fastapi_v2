# alembic init -t async alembic
# alembic downgrade -1
# alembic upgrade head
# alembic revision --autogenerate -m "Create table"
# docker-compose up --build -d
# CREATE TYPE userroleenum AS ENUM ('admin', 'user', 'super_user');

# UPDATE users
# SET user_role = 'super_user'
# WHERE id = 1;

# python -m actions.create_superuser

# INSERT INTO tags (tag_name, tag_color)
# VALUES
# ('black', '#000000'),
# ('grey', '#999999'),
# ('yellow', '#fff000');
# ruff check .  # проверка кода
# ruff format .  # форматирование (как black)
# ruff --fix .  # автоматическое исправление ошибок
