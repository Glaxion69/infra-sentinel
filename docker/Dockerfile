
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml setup.cfg README.md /app/
COPY src /app/src
COPY config /app/config
COPY rules /app/rules
COPY demo /app/demo
RUN pip install --no-cache-dir -e .
ENTRYPOINT ["infra-sentinel"]
CMD ["run", "--config", "config/sentinel.yaml", "--events", "demo/events.jsonl", "--dry-run"]
