### VENV ###

mkdir dj-capstone && cd dj-capstone
git init
python3.14 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip wheel
# If this line errors on Django, rerun with:  pip install --pre "Django>=6.0b1,<6.1"
pip install Django "psycopg[binary]" uvicorn gunicorn black ruff mypy pytest pytest-django django-environ
django-admin startproject app .

### POSTGRES ###

docker run -d --name pg \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=app \
  -p 5432:5432 postgres:16

### DOCKER ###

docker build -t djapp:dev .
docker run --rm -p 8000:8000 --env DB_HOST=host.docker.internal \
  --env DB_USER=postgres --env DB_PASSWORD=postgres --env DB_NAME=app djapp:dev
