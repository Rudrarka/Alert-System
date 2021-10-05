from flask import Blueprint
from modules import app
from flask_cors import CORS, cross_origin
from modules.models import db
from sqlalchemy import text
from collections import defaultdict

CORS(app)
etl_module = Blueprint('etl', __name__)

packet_query = text(""" 
                        select a.id as alert_id, a.user_id as user_id, 
                        a.keyword as keyword, u.email as email, p.id as product_id, 
                        p.product_name as product_name, p.price as price, p.keywords as keywords 
                        from alert a
                        join "user" u  on u.id = a.user_id
                        join product p on a.keyword = ANY(keywords)
                    """) 

@etl_module.route('/packets', methods=['GET'])
@cross_origin()
def get_alerts():
    result = list(db.session.execute(packet_query))
    acc = defaultdict(list)
    for i, r in enumerate(result): acc[r["alert_id"]].append({"product_id":r["product_id"], "product_name":r["product_name"], "keywords":r["keywords"], "price":r["price"]})
    product_packets = [{"alert": k, "products": v} for k, v in acc.items()]
    alert_packet = []
    done_alert = []
    for p in result:
        
        if str(p["alert_id"]) not in done_alert:
            products = next((item["products"] for item in product_packets if str(item["alert"]) == str(p["alert_id"])), None)
            
            if products:
                alert_packet.append({
                "alert_id" : p["alert_id"],
                "user_id" : p["user_id"],
                "keyword" : p["keyword"],
                "email" : p["email"],
                "products": products
            })
            done_alert.append(str(p["alert_id"]))

    return {"res":alert_packet}, 200