import hmac
import sqlite3
import datetime

from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


def fetch_users():
    with sqlite3.connect('point_of_sale.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        new_data = []

        for data in users:
            print(f"{data[0]}, {data[2]}, {data[3]}")
            new_data.append(User(data[0], data[2], data[3]))
    return new_data


def init_user_table():
    conn = sqlite3.connect("point_of_sale.db")
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "name TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("user table created successfully")


def init_product_table():
    conn = sqlite3.connect("point_of_sale.db")
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS product(product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "category TEXT NOT NULL,"
                 "price TEXT NOT NULL,"
                 "description TEXT NOT NULL,"
                 "name TEXT NOT NULL)")
    print("user table created successfully")
    conn.close()


init_user_table()
init_product_table()
users = fetch_users()

username_table = { u.username: u for u in users }
userid_table = { u.id: u for u in users }


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
CORS(app)

jwt = JWT(app, authenticate, identity)


@app.route('/registration/', methods=["POST"])
def user_registration():
    response = {}

    if request.method == "POST":

        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect("point_of_sale.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user("
                           "name,"
                           "username,"
                           "password) VALUES(?, ?, ?)", (name, username, password))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201
        return response


@app.route("/login/", methods=["POST"])
def login():
    response = {}

    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect("point_of_sale.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username='{}' AND password='{}'".format(username, password))
            user_information = cursor.fetchone()

        if user_information:
            response["user_info"] = user_information
            response["message"] = "Success"
            response["status_code"] = 201
            return jsonify(response)

        else:
            response['message'] = "Login Unsuccessful, please try again"
            response['status_code'] = 401
            return jsonify(response)


# cart and product table
@app.route('/viewing/')
def view_products():
    pass


# cart
@app.route('/changing/')
def change_products():
    pass


@app.route('/adding/')
def add_products():
    pass


@app.route('/deleting/<int:item_id>')
def delete_products(item_id):
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()
