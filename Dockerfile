FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

ENV PATH="/app/venv/bin:$PATH"

COPY . /app

EXPOSE 5000

CMD ["/bin/bash", "/app/start.sh"]
