import json


def get_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_list_users(users):
    list_users = []
    for user in users:
        dict_user = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone
        }
        list_users.append(dict_user)
    return list_users


def get_list_orders(orders):
    list_orders = []
    for order in orders:
        dict_order = {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id
        }
        list_orders.append(dict_order)
    return list_orders


def get_list_offers(offers):
    list_offers = []
    for offer in offers:
        dict_offer = {
            "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id
        }
        list_offers.append(dict_offer)
    return list_offers
