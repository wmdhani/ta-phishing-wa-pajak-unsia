@echo off
setlocal
if "%PORT%"=="" set "PORT=8000"
title Cek Pesan Pajak - Server Lokal (127.0.0.1:%PORT%)
cd /d "%~dp0"

set "UVICORN=%LOCALAPPDATA%\venvs\ta-phishing-pajak-unsia\Scripts\uvicorn.exe"
if exist "%UVICORN%" goto :run_uvicorn

if exist "..\..\.venv\Scripts\uvicorn.exe" (
  set "UVICORN=..\..\.venv\Scripts\uvicorn.exe"
  goto :run_uvicorn
)

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
echo Pastikan virtualenv tersedia di "%LOCALAPPDATA%\venvs\ta-phishing-pajak-unsia" atau ".venv",
echo atau jalankan "uv sync" dari folder root proyek.
pause
exit /b 1

:run_uvicorn
echo Menjalankan server Cek Pesan Pajak di http://127.0.0.1:%PORT%/ ...
echo Biarkan jendela ini tetap terbuka selama memakai web atau ekstensi Chrome.
start "" "http://127.0.0.1:%PORT%/"
"%UVICORN%" api:app --host 127.0.0.1 --port %PORT%
