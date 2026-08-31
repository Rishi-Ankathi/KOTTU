# Dockerfile for the Hugging Face Space.
#
# The Space repo (after `populate.mjs` runs) contains:
#   Dockerfile  README.md  requirements.txt  api/  models/
# so the COPY paths below are relative to the Space root, not this repo.
#
# The model runs through the standalone TF-Lite runtime: no TensorFlow, no
# system OpenMP, no src/.

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/    ./api/
COPY models/ ./models/

ENV PYTHONUNBUFFERED=1

EXPOSE 7860
CMD ["sh", "-c", "exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
