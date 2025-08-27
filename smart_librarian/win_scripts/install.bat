@echo off
REM Create venv and install dependencies from the project root
cd /d "%~dp0.."

IF NOT EXIST ".venv" (
  echo [*] Creating virtualenv .venv ...
  py -3 -m venv .venv
)

call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [*] Done installing dependencies.
