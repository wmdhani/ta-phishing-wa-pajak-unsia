FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860

WORKDIR /app

COPY requirements-deploy.txt ./
RUN pip install --no-cache-dir -r requirements-deploy.txt

COPY ["src/eksperimen_baseline.py", "./src/eksperimen_baseline.py"]
COPY ["05 Hasil Evaluasi/tabel_komparasi_utama.csv", "./05 Hasil Evaluasi/tabel_komparasi_utama.csv"]
COPY ["06 Prototipe Aplikasi/", "./06 Prototipe Aplikasi/"]

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

WORKDIR "/app/06 Prototipe Aplikasi"
EXPOSE 7860

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-7860}"]
