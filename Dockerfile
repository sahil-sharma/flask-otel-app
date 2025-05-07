# Builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
  && apt-get -y install libpq-dev gcc \
  && pip install --user -r requirements.txt

# Final
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH="/root/.local/bin:$PATH"

COPY *.py .

EXPOSE 5000

CMD ["python3", "app.py"]
