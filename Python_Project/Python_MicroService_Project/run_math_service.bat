@echo off
setlocal enabledelayedexpansion

echo Starting Math Microservice Setup...

REM Step 1: Check if venv folder exists
IF NOT EXIST "venv_math_service\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv_math_service
) ELSE (
    echo Virtual environment already exists.
)

REM Step 2: Activate virtual environment
echo Activating virtual environment...
call venv_math_service\Scripts\activate

REM Step 3: Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Step 4: Format code with autopep8
echo Formatting code with autopep8...
autopep8 . --in-place --recursive

REM Step 5: Lint code with flake8
echo Running flake8 for style check...
flake8 .

REM Step 6: Run the application
echo Launching Flask microservice...
python main.py

endlocal
