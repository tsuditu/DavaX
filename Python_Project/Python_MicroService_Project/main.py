from flask import Flask
from api.routes import api_router
from db.db import init_db

app = Flask(__name__)
app.register_blueprint(api_router)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
