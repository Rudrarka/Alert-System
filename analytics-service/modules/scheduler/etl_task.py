import logging
# from modules import celery_app
from flask import current_app
from modules.models import Alert, db, Product, User, Price, ProductPrice
# from modules import scheduler
from modules.utils.rest_utils import AlertApi

def get_app():
    from modules import app
    return app

def create_alert(item):
    return Alert(
        id=item["alert_id"],
        keyword=item["keyword"],
        user_id=item["user_id"]
    )

def create_or_update_alert(item):
    alert = db.session.query(Alert).filter(Alert.id==item["alert_id"]).one_or_none()
    if alert:
        alert.keyword=item["keyword"]
    else:
        alert = create_alert(item)
        db.session.add(alert)

def create_user(item):
    return User(
        id=item["user_id"],
        email=item["email"]
    )

def add_user(item):
    user = db.session.query(User).filter(User.id==item["user_id"]).one_or_none()
    if not user:
        user = create_user(item)
        db.session.add(user)

def create_product(product, price):
    return Product(
        id = product["product_id"],
        price = price,
        keywords = product["keywords"],
        product_name = product["product_name"]
    )

def create_product_price_rel(product, price):
    product_price = ProductPrice(
        product_id=str(product.id),
        price_id=str(price.id)
    )
    db.session.add(product_price)

def add_or_update_product(updated_product, price):
    product = db.session.query(Product).filter(Product.id==updated_product["product_id"]).one_or_none()
    if product:
        product.keywords = updated_product["keywords"]
        product.price = price
        product.product_name = updated_product["product_name"]
    else:
        product = create_product(updated_product, price)
    
    db.session.add(product)
    db.session.flush()
    create_product_price_rel(product, price)

def add_price(product):
    price = db.session.query(Price).filter(Price.price==product["price"]).one_or_none()
    if not price:
        price = Price(
            price=product["price"]
        )
        db.session.add(price)
        db.session.flush()
    return price

def add_packet(item):
    with get_app().app_context():
        add_user(item)
        create_or_update_alert(item)
        for product in item["products"]:
            price = add_price(product)
            add_or_update_product(product, price)
        
        db.session.commit()

# @scheduler.task("cron", id="do_job_2", second="2")
def etl():
    print('in job')
    packets = AlertApi().get_packets()
    print(packets)
    for item in packets["res"]:
        add_packet(item)

    
    # scheduler.add_job()
    # print("add in celery queue")
    # print(kwargs)
    # id = kwargs["id"]
    # keyword = kwargs["keyword"]
    # email = kwargs["user_email"]
    # products = db.session.query(Product).filter(Product.keywords.any(keyword)).all()
    # items = [p.as_json() for p in products]
    # print("============")
    # print(items)

    # celery_app.send_task(
    #     'task.send_email', 
    #     kwargs={
    #         "trigger_id": id,
    #         'reciever': email,
    #         "type": "alert",
    #         "subject": "Alert",
    #         "items":items
    #     })

def add_product(product, keyword):
    return Product(
        id=product["id"],
        product_name=product["product_name"],
        price=product["price"],
        keywords=[keyword]
    )

def persist_products(products, keyword):
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

# def search_products(*args):
#     try:
#         products = MockerApi().search_products(args[0])
#         persist_products(products, args[0])
#         # scheduler.add_job(id = args[1]["id"], func = scheduledTask, kwargs=args[1], trigger = 'interval', seconds = interval)
#     except Exception as e:
#         logging.error(e)