from dotenv import dotenv_values
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

config = dotenv_values(".env")

app.config["SQLALCHEMY_DATABASE_URI"] = config.get('db.uri')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
session = db.session
