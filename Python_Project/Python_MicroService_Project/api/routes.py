from flask import Blueprint, request, render_template
from pydantic import ValidationError
from db.db import save_request, export_requests_to_txt
from services.fibonacci_service import compute_fibonacci
from services.factorial_service import compute_factorial
from services.pow_service import compute_pow
from models.request_model import FibonacciInput, FactorialInput, PowInput

api_router = Blueprint('api', __name__)

# --------------------------
# HOME PAGE
# --------------------------


@api_router.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

# --------------------------
# FACTORIAL
# --------------------------


@api_router.route("/factorial-form", methods=["GET"])
def factorial_form_page():
    return render_template("factorial_form.html", result=None)


@api_router.route("/factorial-form", methods=["POST"])
def factorial_form_post():
    try:
        n = int(request.form.get("n"))
        FactorialInput(n=n)  # Validate with Pydantic
        result = compute_factorial(n)
        save_request("factorial", f"n={n}", str(result))
        export_requests_to_txt()
    except (ValueError, ValidationError):
        result = "Error! Please enter a valid number."
    return render_template("factorial_form.html", result=result)

# --------------------------
# FIBONACCI
# --------------------------


@api_router.route("/fibonacci-form", methods=["GET"])
def fibonacci_form_page():
    return render_template("fibonacci_form.html", result=None)


@api_router.route("/fibonacci-form", methods=["POST"])
def fibonacci_form_post():
    try:
        n = int(request.form.get("n"))
        FibonacciInput(n=n)  # Validate with Pydantic
        result = compute_fibonacci(n)
        save_request("fibonacci", f"n={n}", str(result))
        export_requests_to_txt()
    except (ValueError, ValidationError):
        result = "Error! Please enter a valid number."
    return render_template("fibonacci_form.html", result=result)

# --------------------------
# POW (x^y)
# --------------------------


@api_router.route("/pow-form", methods=["GET"])
def pow_form_page():
    return render_template("pow_form.html", result=None)


@api_router.route("/pow-form", methods=["POST"])
def pow_form_post():
    try:
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        PowInput(x=x, y=y)  # Validate with Pydantic
        result = compute_pow(x, y)
        save_request("pow", f"x={x}, y={y}", str(result))
        export_requests_to_txt()
    except (ValueError, ValidationError):
        result = "Error! Please enter valid numbers."
    return render_template("pow_form.html", result=result)
