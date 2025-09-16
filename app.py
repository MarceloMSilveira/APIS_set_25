from flask import Flask
from config_db import db
from flask_migrate import Migrate



app=Flask(__name__)
app.config.from_object('config')

db.init_app(app)

migrate = Migrate(app,db)

from models import Plant

with app.app_context():
    db.create_all()

