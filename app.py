from flask import Flask, jsonify, request, abort
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError, fields

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+mysqlconnector://root:@localhost/e_commerce_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
