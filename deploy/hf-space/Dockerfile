# Dockerfile for the Hugging Face Space.
#
# The Space repo (after `populate.mjs` runs) contains:
#   Dockerfile  README.md  requirements.txt  api/  src/  models/
# so the COPY paths below are relative to the Space root, not this repo.

FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/    ./api/
COPY src/    ./src/
COPY models/ ./models/

ENV TF_CPP_MIN_LOG_LEVEL=2 \
    TF_ENABLE_ONEDNN_OPTS=0 \
    PYTHONUNBUFFERED=1

EXPOSE 7860
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
