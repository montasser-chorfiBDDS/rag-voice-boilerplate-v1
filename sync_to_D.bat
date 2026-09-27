@echo off
chcp 65001 >nul
title Sync: C (Main) -> D (Backup)
echo ================================================================
echo   Palmera RAG - Synchronization
echo   Source (Main)   : C:\Users\pc\.gemini\antigravity\scratch\rag-voice-boilerplate-v1
echo   Destination     : D:\rag-voice-boilerplate-v1  (Backup copy)
echo ================================================================
echo.

set "SRC=C:\Users\pc\.gemini\antigravity\scratch\rag-voice-boilerplate-v1"
set "DST=D:\rag-voice-boilerplate-v1"

if not exist "%SRC%" (
    echo [ERROR] Source folder not found: %SRC%
    pause
    exit /b 1
)

if not exist "%DST%" (
    echo [INFO] Destination folder not found. Creating: %DST%
    mkdir "%DST%"
)

echo [1/4] Copying project files (excluding venv_rag, .git, __pycache__, .env) ...
robocopy "%SRC%" "%DST%" /E /XD "%SRC%\venv_rag" "%SRC%\.git" "%SRC%\__pycache__" "%SRC%\data\vector_store" "%SRC%\docker\data" "%SRC%\.claude" "%SRC%\.agents" /XF "*.pyc" "*.pyo" ".env" ".env.local" /NFL /NDL /NJH /NJS /NP

echo.
echo [2/4] Ensuring 'data' folder text files are copied ...
robocopy "%SRC%\data" "%DST%\data" /E /XF "*.faiss" "*.pkl" /NFL /NDL /NJH /NJS /NP

echo.
echo [3/4] Syncing vector index (FAISS store) from C -> D ...
robocopy "%SRC%\data\vector_store" "%DST%\data\vector_store" /MIR /NFL /NDL /NJH /NJS /NP

echo.
echo [4/4] Done copying.
echo         NOTE: Your local 'venv_rag', '.env', '.git' stay untouched in D.
echo         The 'data\vector_store' is now kept in sync from C.
echo.
echo [5/5] Synchronization complete!
echo ================================================================
echo   Backup updated from C -^> D
echo   Check files at: %DST%
echo ================================================================
pause
