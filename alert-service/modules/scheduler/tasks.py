import logging
from modules import celery_app, app
from modules.models import db, Product
from modules.utils.rest_utils import MockerApi
from sqlalchemy import asc

def scheduledTask(**kwargs):
    id = kwargs["id"]
    keyword = kwargs["keyword"]
    email = kwargs["user_email"]
    with app.app_context():
        products = db.session.query(Product).filter(Product.keywords.any(keyword)).order_by(asc(Product.price)).all()
    items = [p.as_json() for p in products]

    celery_app.send_task(
        'task.send_email', 
        kwargs={
            "trigger_id": id,
            'reciever': email,
            "type": "alert",
            "subject": "Alert",
            "items":items
        })

def add_product(product, keyword):
    return Product(
        id=product["id"],
        product_name=product["product_name"],
        price=product["price"],
        keywords=[keyword]
    )

def persist_products(products, keyword):
    with app.app_context():
        for product in products:
            p = db.session.query(Product).filter(Product.id==product["id"]).one_or_none()
            if p and (keyword not in p.keywords):
                p.keywords = p.keywords + [keyword]
                print(p.keywords)
            elif not p:
                p = add_product(product, keyword)
            print(p.keywords)
            db.session.add(p)
        db.session.commit()

def search_products(*args):
    try:
        products = MockerApi().search_products(args[0])
        persist_products(products, args[0])
        # scheduler.add_job(id = args[1]["id"], func = scheduledTask, kwargs=args[1], trigger = 'interval', seconds = interval)
    except Exception as e:
        logging.error(e)