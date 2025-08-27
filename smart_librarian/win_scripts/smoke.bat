@echo off
cd /d "%~dp0.."
call ".venv\Scripts\activate.bat"
set "PYTHONPATH=%cd%"

python tests\smoke_retrieval.py %*
