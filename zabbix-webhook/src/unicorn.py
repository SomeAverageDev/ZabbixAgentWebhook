from flask.cli import FlaskGroup
from app import app
import os


debug = int(os.environ.get("DEBUG", default=0))

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
