
def build_analytics_mail(items):
    body = ""
    for item in items:
        status = "increased" if item["change_percent"] > 0 else "decreased"
        body = f"{body} Price of {item['product_name']} is {status} by {abs(item['change_percent'])}% \n"
    return body

def build_alert_mail(items):
    body = ""
    for item in items:
        body = f"{body} Price of {item['product_name']} is {item['price']} \n"
    return body

def build_body(data):
    body = None
    if data["type"] == 'alert':
        body = build_alert_mail(data["items"])
    elif data["type"] == "analytics":
        body = build_analytics_mail(data["items"])

    return body