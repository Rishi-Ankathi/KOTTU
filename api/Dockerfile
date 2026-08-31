# Container image for the KOTTU API.
#
# Build from the REPO ROOT so it can copy models/ next to api/:
#
#   docker build -f api/Dockerfile -t kottu-api .
#   docker run --rm -p 7860:7860 kottu-api
#   # then open http://localhost:7860/docs
#
# The model runs through the standalone TF-Lite runtime, so the image needs
# neither TensorFlow nor a system OpenMP library. src/ is not copied - the API
# only reads the exported artifacts in models/.

FROM python:3.11-slim
# Minimal Debian + Python 3.11. "slim" drops compilers, man pages, extras.

WORKDIR /app
# All commands below run here, and it's the container's start directory.

# ---- dependencies (separate layer: cached until requirements.txt changes) ---
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- application ----------------------------------------------------------------
COPY api/    ./api/
COPY models/ ./models/
# models/ needs kottu_model.tflite + serving_params.json (from
# scripts/export_serving.py). scaler.pkl / label_encoder.pkl / the .keras model
# are not used at runtime.

# ---- runtime ------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1
# Unbuffered stdout so container logs appear immediately.

EXPOSE 7860
# Default port (Hugging Face Spaces expects 7860). Hosts that assign a port at
# runtime - Render, Cloud Run - set $PORT, which the command below honours.

CMD ["sh", "-c", "exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
# 0.0.0.0 = listen on every interface (required inside a container); exec so
# uvicorn becomes PID 1 and receives stop signals directly.
