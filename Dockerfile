FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /PythonProject5

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=/root/.cache/poetry \
    pip install --no-cache-dir poetry && \
    poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --without-hashes > requirements.txt && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


FROM python:3.13-slim

WORKDIR /PythonProject5

RUN apt-get update && apt-get install -y --no-install-recommends curl netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system PythonProject5 && adduser --system --group PythonProject5

COPY --from=builder /wheels /wheels
COPY --from=builder /PythonProject5/requirements.txt ./
COPY . .

RUN pip install --no-cache-dir --find-links=/wheels -r requirements.txt

RUN chown -R PythonProject5:PythonProject5 /PythonProject5 && chmod -R 755 /PythonProject5

USER PythonProject5
