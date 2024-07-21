FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY load_balancer.py consistent_hash.py ./

RUN apt-get update && apt-get install -y docker.io

CMD ["python", "load_balancer.py"]