from modules import sio_conn
from modules.utils.util_funcs import update_product_if_present

@sio_conn.event
def handle_connect():
    """
    Handles connection request from server 
    """
    print('connected')

@sio_conn.event
def product_updated():
    print('updated')
    updated_product = {
    "id": "7c28737c-d590-438b-bd7a-e7a8db46315b",
    "product_name": "Wine - Chablis J Moreau Et Fils",
    "price": 4
  }
    update_product_if_present(updated_product)