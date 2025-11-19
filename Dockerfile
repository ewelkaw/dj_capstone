# --- build stage ---
FROM python:3.14-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y postgresql-client
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
# create non-root user
RUN useradd -m appuser
COPY . /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz')"
CMD ["gunicorn","app.wsgi:application","--bind","0.0.0.0:8000","--workers","2"]
