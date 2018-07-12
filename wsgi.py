# wsgi.py
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass # Heroku does not use .env

from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)
