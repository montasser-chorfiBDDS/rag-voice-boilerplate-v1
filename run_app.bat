@echo off
title RAG Voice Boilerplate - Launcher
cd /d "%~dp0"
echo ========================================================
echo   Starting Enterprise RAG Application (Backend + UI)
echo ========================================================
echo.

echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "FastAPI Backend" /min "C:\vr\Scripts\uvicorn.exe" main:app --host 0.0.0.0 --port 8000

echo [2/2] Starting Streamlit Frontend on http://localhost:8501 ...
timeout /t 3 /nobreak >nul
start "Streamlit UI" "C:\vr\Scripts\streamlit.exe" run app_ui.py --server.port 8501

echo.
echo ========================================================
echo   Application Launched Successfully!
echo   Browser will open at http://localhost:8501
echo ========================================================
pause
