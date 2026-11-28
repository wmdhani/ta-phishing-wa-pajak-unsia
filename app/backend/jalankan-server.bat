@echo off
setlocal
if "%PORT%"=="" set "PORT=8000"
title Cek Pesan Pajak - Server Lokal (127.0.0.1:%PORT%)
cd /d "%~dp0"
set "UV_PROJECT_ENVIRONMENT=%LOCALAPPDATA%\venvs\ta-phishing-pajak-unsia"

set "UVICORN=%UV_PROJECT_ENVIRONMENT%\Scripts\uvicorn.exe"
if exist "%UVICORN%" goto :run_uvicorn

where uv >nul 2>nul
if %errorlevel%==0 (
  echo Menjalankan server Cek Pesan Pajak via uv di http://127.0.0.1:%PORT%/ ...
  echo Biarkan jendela ini tetap terbuka selama memakai web atau ekstensi Chrome.
  start "" "http://127.0.0.1:%PORT%/"
  uv run uvicorn api:app --host 127.0.0.1 --port %PORT%
  exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
  python -c "import uvicorn" >nul 2>nul
  if %errorlevel%==0 (
    echo Menjalankan server Cek Pesan Pajak via python di http://127.0.0.1:%PORT%/ ...
    echo Biarkan jendela ini tetap terbuka selama memakai web atau ekstensi Chrome.
    start "" "http://127.0.0.1:%PORT%/"
    python -m uvicorn api:app --host 127.0.0.1 --port %PORT%
    exit /b %errorlevel%
  )
)

echo Virtual environment atau uvicorn tidak ditemukan.
echo Pastikan virtualenv tersedia di "%UV_PROJECT_ENVIRONMENT%",
echo atau jalankan "set UV_PROJECT_ENVIRONMENT=%UV_PROJECT_ENVIRONMENT% && uv sync" dari folder root proyek.
pause
exit /b 1

:run_uvicorn
echo Menjalankan server Cek Pesan Pajak di http://127.0.0.1:%PORT%/ ...
echo Biarkan jendela ini tetap terbuka selama memakai web atau ekstensi Chrome.
start "" "http://127.0.0.1:%PORT%/"
"%UVICORN%" api:app --host 127.0.0.1 --port %PORT%
