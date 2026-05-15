FROM python:3.12-slim

ARG UID=1000
ARG GID=1000

RUN groupadd -g ${GID} appgroup \
 && useradd -u ${UID} -g ${GID} -m appuser

WORKDIR /app
ENV CONTENT_DIR=/docs
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
