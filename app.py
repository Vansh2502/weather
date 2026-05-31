from flask import Flask

from backend.controllers.user_controller import (
    user_bp
)

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

app.register_blueprint(
    user_bp
)

if __name__ == "__main__":
    app.run(debug=True)