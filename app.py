from flask import Flask, jsonify, request, redirect, render_template, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import utils

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.relationship("Order")
    user = db.relationship("User")


# db.drop_all()
db.create_all()


def get_users():
    users = []
    data = utils.get_from_json("users.json")
    for item in data:
        user = User(
            id=item['id'],
            first_name=item['first_name'],
            last_name=item['last_name'],
            age=item['age'],
            email=item['email'],
            role=item['role'],
            phone=item['phone']
        )
        users.append(user)
    return users


def get_orders():
    orders = []
    data = utils.get_from_json("orders.json")
    for item in data:
        order = Order(
            id=item['id'],
            name=item['name'],
            description=item['description'],
            start_date=datetime.strptime(item['start_date'], "%m/%d/%Y"),
            end_date=datetime.strptime(item['end_date'], "%m/%d/%Y"),
            address=item['address'],
            price=item['price'],
            customer_id=item['customer_id'],
            executor_id=item['executor_id']
        )
        orders.append(order)
    return orders


def get_offers():
    offers = []
    data = utils.get_from_json("offers.json")
    for item in data:
        offer = Offer(
            id=item['id'],
            order_id=item['order_id'],
            executor_id=item['executor_id']
        )
        offers.append(offer)
    return offers


@app.route('/')
def index_page():
    return render_template("index.html")


@app.route('/import-data/')
def import_data():
    db.drop_all()
    db.create_all()

    users = get_users()
    db.session.add_all(users)

    orders = get_orders()
    db.session.add_all(orders)

    offers = get_offers()
    db.session.add_all(offers)

    db.session.commit()

    users = db.session.query(User).all()
    users = utils.get_list_users(users)
    orders = db.session.query(Order).all()
    orders = utils.get_list_orders(orders)
    offers = db.session.query(Offer).all()
    offers = utils.get_list_offers(offers)

    response = [users, orders, offers]
    return jsonify(response)


@app.route('/users/', methods=['GET', 'POST'])
def users_page():
    if request.method == 'GET':
        users = db.session.query(User).all()
        users = utils.get_list_users(users)
        return jsonify(users)
    if request.method == 'POST':
        data = request.json
        users = []
        for item in data:
            user = User(
                first_name=item['first_name'],
                last_name=item['last_name'],
                age=item['age'],
                email=item['email'],
                role=item['role'],
                phone=item['phone']
            )
            users.append(user)

        db.session.add_all(users)
        db.session.commit()
        return redirect("/users/")


@app.route('/users/<int:user_id>/', methods=['GET', 'PUT', 'DELETE'])
def user_page(user_id):
    if request.method == 'GET':
        user = db.session.query(User).filter(User.id == user_id).all()
        user = utils.get_list_users(user)
        return jsonify(user[0])
    if request.method == 'PUT':
        data = request.json
        user = User.query.get(user_id)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']
        db.session.add(user)
        db.session.commit()
        return redirect(f'/users/{user_id}/')
    if request.method == 'DELETE':
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(f'/users/')


@app.route('/orders/', methods=['GET', 'POST'])
def orders_page():
    if request.method == 'GET':
        orders = db.session.query(Order).all()
        orders = utils.get_list_orders(orders)
        return jsonify(orders)
    if request.method == 'POST':
        data = request.json
        orders = []
        for item in data:
            order = Order(
                name=item['name'],
                description=item['description'],
                start_date=datetime.strptime(item['start_date'], "%m/%d/%Y"),
                end_date=datetime.strptime(item['end_date'], "%m/%d/%Y"),
                address=item['address'],
                price=item['price'],
                customer_id=item['customer_id'],
                executor_id=item['executor_id']
            )
            orders.append(order)

        db.session.add_all(orders)
        db.session.commit()
        return redirect("/orders/")


@app.route('/orders/<int:order_id>/', methods=['GET', 'PUT', 'DELETE'])
def order_page(order_id):
    if request.method == 'GET':
        order = db.session.query(Order).filter(Order.id == order_id).all()
        order = utils.get_list_orders(order)
        return jsonify(order[0])
    if request.method == 'PUT':
        data = request.json
        order = Order.query.get(order_id)
        order.address = data['address']
        order.customer_id = data['customer_id']
        order.description = data['description']
        order.end_date = datetime.strptime(data['end_date'], "%m/%d/%Y")
        order.executor_id = data['executor_id']
        order.name = data['name']
        order.price = data['price']
        order.start_date = datetime.strptime(data['start_date'], "%m/%d/%Y")
        db.session.add(order)
        db.session.commit()
        return redirect(f'/orders/{order_id}/')
    if request.method == 'DELETE':
        order = Order.query.get(order_id)
        db.session.delete(order)
        db.session.commit()
        return redirect(f'/orders/')


@app.route('/offers/', methods=['GET', 'POST'])
def offers_page():
    if request.method == 'GET':
        offers = db.session.query(Offer).all()
        offers = utils.get_list_offers(offers)
        return jsonify(offers)
    if request.method == 'POST':
        data = request.json
        offers = []
        for item in data:
            offer = Offer(
                order_id=item['order_id'],
                executor_id=item['executor_id']
            )
            offers.append(offer)

        db.session.add_all(offers)
        db.session.commit()
        return redirect('/offers/')


@app.route('/offers/<int:offer_id>/', methods=['GET', 'PUT', 'DELETE'])
def offer_page(offer_id):
    if request.method == 'GET':
        offer = db.session.query(Offer).filter(Offer.id == offer_id).all()
        offer = utils.get_list_offers(offer)
        return jsonify(offer[0])
    if request.method == 'PUT':
        data = request.json
        offer = Offer.query.get(offer_id)
        offer.executor_id = data['executor_id']
        offer.order_id = data['order_id']
        db.session.add(offer)
        db.session.commit()
        return redirect(f'/offers/{offer_id}/')
    if request.method == 'DELETE':
        offer = Offer.query.get(offer_id)
        db.session.delete(offer)
        db.session.commit()
        return redirect('/offers/')


if __name__ == '__main__':
    app.run()
