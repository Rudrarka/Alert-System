import logging

from flask import app
from modules.models import Product, db
from modules import app
import logging

def update_product_if_present(updated_product):
    try:
        with app.app_context():
            product = db.session.query(Product).filter(Product.id==updated_product["id"]).one_or_none()
            if product:
                product.price=updated_product["price"]
                product.product_name = updated_product["product_name"]
                db.session.add(product)
                db.session.commit()
    except Exception as e:
        logging.error(e)
