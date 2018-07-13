# wsgi.py
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass # Heroku does not use .env

from flask import Flask, request
from config import Config
app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema
from schemas import product_schema

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

@app.route('/api/v1/products/<id>')
def get_product(id):
    product = db.session.query(Product).get(int(id))
    return product_schema.jsonify(product)

@app.route('/api/v1/products', methods=['POST'])
def add_product():
    new_product = Product()
    new_product.name = request.form['name']
    new_product.description = request.form['description']
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route('/api/v1/products', methods=['PATCH'])
def update_product():
    new_product = Product()
    new_product.name = request.form['name']
    new_product.description = request.form['description']
    db.session.query(Product).filter_by(name=new_product.name).update({"description" : new_product.description})
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route('/api/v1/products/<id>', methods=['DELETE'])
def delete_product(id):
    db.session.query(Product).filter_by(id=id).delete()
    db.session.commit()
    return ('', 200)

