FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENV GROQ_API_KEY=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
# Install PostgreSQL client tools (including pg_config)
RUN apt-get update && apt-get install -y libpq-dev
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

