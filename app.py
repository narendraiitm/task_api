from config import DevelopmentConfig
from flask import Flask
from app.models import db
from app.resources import api
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    return app


app = create_app()


@app.before_first_request
def create_db():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True, port='5001', host='0.0.0.0')