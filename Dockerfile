# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY server.py .

RUN pip install Flask

ENV SERVER_ID 1

EXPOSE 5000

CMD ["python", "server.py"]
