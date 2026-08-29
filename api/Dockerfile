# Container image for the KOTTU API.
#
# Build from the REPO ROOT so it can copy src/ and models/ next to api/:
#
#   docker build -f api/Dockerfile -t kottu-api .
#   docker run --rm -p 7860:7860 kottu-api
#   # then open http://localhost:7860/docs
#
# Hugging Face Spaces (Docker SDK) builds this automatically and routes to 7860.

# ---- base -------------------------------------------------------------------
FROM python:3.11-slim
# Minimal Debian + Python 3.11. "slim" drops compilers, man pages, extras.

# TensorFlow's CPU kernels link against OpenMP; the slim image lacks its runtime.
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# All commands below run here, and it's the container's start directory - so
# `from src.predict import Predictor` resolves when uvicorn runs.

# ---- dependencies (separate layer: cached until requirements.txt changes) ---
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- application ----------------------------------------------------------------
COPY api/    ./api/
COPY src/    ./src/
COPY models/ ./models/

# ---- runtime ------------------------------------------------------------------
ENV TF_CPP_MIN_LOG_LEVEL=2 \
    TF_ENABLE_ONEDNN_OPTS=0 \
    PYTHONUNBUFFERED=1
# Quiet TensorFlow's startup logs; disable oneDNN for reproducible numbers;
# unbuffered stdout so container logs appear immediately.

EXPOSE 7860
# Documentation; also the port Hugging Face Spaces expects.

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
# 0.0.0.0 = listen on every interface (required inside a container).
