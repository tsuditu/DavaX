# Math Microservice – Flask + SQLite + Pydantic

This project implements a Python-based microservice that exposes simple mathematical operations through a web interface. It supports:

- Power (x ^ y)
- Fibonacci (n-th number)
- Factorial (n!)

Each operation is validated, logged to an SQLite database, and exported to a `.txt` file as a Pandas DataFrame.

## Features

- Web interface built with Flask
- Input validation using Pydantic
- SQLite database to store every request
- Request logs exported to `requests_log.txt` as a Pandas DataFrame
- Code linted with `flake8` and auto-formatted with `autopep8`
- Optional automation via `.bat` script for Windows

## Technologies Used

| Category           | Technology     |
|--------------------|----------------|
| Web Framework      | Flask          |
| Data Validation    | Pydantic       |
| Database           | SQLite         |
| Templates (HTML)   | Jinja2         |
| Code Linter        | flake8         |
| Code Formatter     | autopep8       |

## Project Structure

project/
- main.py                   # Entry point
- api/
  - routes.py               # Routes and logic
- services/
  - fibonacci.py
  - factorial.py
  - pow.py
- models/
  - request_model.py        # Pydantic input models
- db/
  - db.py                   # DB logic + export to .txt
  - history.db              # Auto-generated database
- templates/
  - index.html
  - fibonacci_form.html
  - factorial_form.html
  - pow_form.html
- requests_log.txt          # Auto-generated log after each request
- requirements.txt
- .flake8
- README.md
- run_math_service.bat      # Automation script for Windows

## Running the Application (Windows)

### Option 1: Use the batch script

Run the following in CMD or double-click:

    run_math_service.bat

This will:

- Create virtual environment if missing
- Install all dependencies
- Format code with `autopep8`
- Lint code with `flake8`
- Start the Flask web server

### Option 2: Run manually

    python -m venv venv_math_service
    venv_math_service\Scripts\activate
    pip install -r requirements.txt
    autopep8 . --in-place --recursive
    flake8 .
    python main.py

## Available Routes

- `/` – Homepage with links to each operation
- `/fibonacci-form` – Input form for Fibonacci
- `/factorial-form` – Input form for Factorial
- `/pow-form` – Input form for Power

Each operation is validated with Pydantic, saved in `history.db`, and the full log is exported to `requests_log.txt`.

## Code Quality

Run the following to check or auto-format your code:

    flake8 .
    autopep8 . --in-place --recursive