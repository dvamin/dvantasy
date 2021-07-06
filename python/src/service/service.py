from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from logging import getLogger, INFO
import os
from python.src.data.database import db
from python.src.service.blueprints.league.league import league_bp
from python.src.service.setup_logging import configure_logging

configure_logging("python", INFO)

LOGGER = getLogger("python.src.service.service")

LOGGER.info("Starting Flask App")

app = Flask("dvantasy")
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

LOGGER.info("Registering blueprints")

app.register_blueprint(league_bp, url_prefix="/league")
api = Api(league_bp)
api.init_app(app)

if __name__ == "__main__":
    app.run()