FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY server/ server/
COPY app/tarot_prompt_template.txt app/

COPY app/.env .env

EXPOSE 8000

CMD ["uvicorn", "server.api:app", "--host", "0.0.0.0", "--port", "8000"]