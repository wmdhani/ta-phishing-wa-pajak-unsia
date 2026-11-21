FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860

WORKDIR /app

COPY requirements-deploy.txt ./
RUN pip install --no-cache-dir -r requirements-deploy.txt

COPY ["ml/eksperimen_baseline.py", "./ml/eksperimen_baseline.py"]
COPY ["05-hasil-evaluasi/csv/tabel_komparasi_utama.csv", "./05-hasil-evaluasi/csv/tabel_komparasi_utama.csv"]
COPY ["05-hasil-evaluasi/json/benchmark_latensi_purwarupa.json", "./05-hasil-evaluasi/json/benchmark_latensi_purwarupa.json"]
COPY ["app/", "./app/"]

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

WORKDIR "/app/app/backend"
EXPOSE 7860

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-7860}"]
