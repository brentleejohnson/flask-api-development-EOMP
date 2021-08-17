# Brent Lee Johnson ==> Class 1
# Flask API Development EOMP
# All imports
import hmac
import sqlite3
import datetime

from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from flask_mail import Mail, Message

import cloudinary
import cloudinary.uploader
# import DNS
# import validate_email


# User class
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# Product class
class Product(object):
    def __init__(self, user_id, product_image_url, product_name, product_description, product_price, product_category):
        self.user_id = user_id
        self.product_image_url = product_image_url
        self.product_name = product_name
        self.product_description = product_description
        self.product_price = product_price
        self.product_category = product_category


# Database class
class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect("point_of_sale.db")
        self.cursor = self.conn.cursor()

    def registration(self, name, email, username, password):
        # Sending user info to database
        self.cursor.execute("INSERT INTO user("
                            "name,"
                            "email,"
                            "username,"
                            "password) VALUES(?, ?, ?, ?, ?)", (name, email, username, password))
        self.conn.commit()

    # Add product to database
    def add_product(self, user_id, product_image, product_name, product_description, product_price, product_category):

        # Upload image to cloudinary
        cloudinary.config(cloud_name='ddvdj4vy6', api_key='416417923523248',
                          api_secret='v_bGoSt-EgCYGO2wIkFKRERvqZ0')
        upload_result = None

        app.logger.info('%s file_to_upload', product_image)
        if product_image:
            upload_result = cloudinary.uploader.upload(product_image)   # Upload results
            app.logger.info(upload_result)
            # data = jsonify(upload_result)
        self.cursor.execute("INSERT INTO product (user_id, product_name, product_image_url, product_category, "
                            "product_description, product_price) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_id, upload_result['url'], product_name, product_description, product_price,
                             product_category))

        self.conn.commit()

    # fetch products
    def get_products(self):
        self.cursor.execute("SELECT * FROM product")
        return self.cursor.fetchall()

    # fetch one specific product
    def view_product(self, product_id):
        self.cursor.execute('SELECT * FROM product WHERE product_id={}'.format(product_id))
        return self.cursor.fetchone()

    # edit product
    def edit_product(self, product_data, product_id):
        response = {}
        put_data = {}

        # if statements are to check if data received is not empty
        if product_data.get('product_name'):
            put_data['product_name'] = product_data.get('product_name')
            with sqlite3.connect('point_of_sale.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET product_name=? WHERE product_id=?", (put_data["product_name"],
                                                                                        product_id))
                conn.commit()
                response['message'] = "Update was successful"
                response['status_code'] = 200

        #
        if product_data.get('product_category'):
            put_data['product_category'] = product_data.get('product_category')
            with sqlite3.connect('point_of_sale.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET product_category=? WHERE product_id=?",
                               (put_data["product_category"], product_id))
                conn.commit()
                response['message'] = "Update was successful"
                response['status_code'] = 200

        if product_data.get('product_description'):
            put_data['product_description'] = product_data.get('product_description')
            with sqlite3.connect('point_of_sale.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET product_description=? WHERE product_id=?",
                               (put_data["product_description"], product_id))
                conn.commit()
                response['message'] = "Update was successful"
                response['status_code'] = 200

        if product_data.get('product_price'):
            put_data['product_price'] = product_data.get('product_price')
            with sqlite3.connect('point_of_sale.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET product_price=? WHERE product_id=?", (put_data["product_price"],
                                                                                         product_id))
                conn.commit()
                response['message'] = "Update was successful"
                response['status_code'] = 200

        return response

    def edit_profile(self, user_data, user_id):
        response = {}
        put_data = {}

        # if statements are to check if data received is not empty
        if user_data.get('name'):
            put_data['name'] = user_data.get('name')
            with sqlite3.connect('point_of_sale.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET name=? WHERE user_id=?", (put_data["name"], user_id))
                conn.commit()
                response['message'] = "Update was successful"
                response['status_code'] = 200

        if user_data.get('email'):
            put_data['email'] = user_data.get('email')
            with sqlite3.connect('point_of_sale.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET email=? WHERE user_id=?",
                               (put_data["email"], user_id))
                conn.commit()
                response['message'] = "Update was successful"
                response['status_code'] = 200

        if user_data.get('username'):
            put_data['username'] = user_data.get('username')
            with sqlite3.connect('point_of_sale.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET username=? WHERE user_id=?", (put_data["username"],user_id))
                conn.commit()
                response['message'] = "Update was successful"
                response['status_code'] = 200

        if user_data.get('password'):
            put_data['password'] = user_data.get('password')
            with sqlite3.connect('point_of_sale.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET password=? WHERE user_id=?", (put_data["password"],user_id))
                conn.commit()
                response['message'] = "Update was successful"
                response['status_code'] = 200

        return response

    # Delete product
    def delete_product(self, product_id):
        with sqlite3.connect('point_of_sale.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM product WHERE product_id={}'.format(product_id))
            conn.commit()


# Fetching the information from the user table in the database
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


# Creating the user table
def init_user_table():
    conn = sqlite3.connect("point_of_sale.db")
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "name TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("user table created successfully")


# Creating the product table
def init_product_table():
    conn = sqlite3.connect("point_of_sale.db")
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS product(product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "category TEXT NOT NULL,"
                 "name TEXT NOT NULL,"
                 "price TEXT NOT NULL,"
                 "description TEXT NOT NULL)")
    print("user table created successfully")
    conn.close()


# Calling the tables from the database
init_user_table()
init_product_table()
users = fetch_users()

username_table = { u.username: u for u in users }
userid_table = { u.id: u for u in users }


# Authentication
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


# Containing information that is compulsory for allowing the email to work
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# This allows for the token key to have an extended time limit
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=4000)
CORS(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "huntermoonspear@gmail.com"
app.config['MAIL_PASSWORD'] = "dianadragonheart"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

jwt = JWT(app, authenticate, identity)


# Registration with email if successful
@app.route('/registration/', methods=["POST"])
def user_registration():
    response = {}

    if request.method == "POST":

        name = request.json["name"]
        username = request.json["username"]
        password = request.json["password"]
        email = request.json["email"]

        with sqlite3.connect("point_of_sale.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user("
                           "name,"
                           "username,"
                           "password,"
                           "email) VALUES(?, ?, ?, ?)", (name, username, password, email))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201
            # Email IF the registration works
            if response["status_code"] == 201:
                msg = Message("Hello Message", sender="huntermoonspear@gmail.com", recipients=[email])
                msg.body = "My email using Flask"
                mail.send(msg)
                return "Message sent"


# @app.route('/email/<email>', methods=['GET'])
# def send_email(email):
#     mail = Mail(app)
#
#     msg = Message('Hello Message', sender='lottoemail123@gmail.com', recipients=[email])
#     msg.body = "This is the email body after making some changes"
#     mail.send(msg)
#
#     return "sent"


@app.route("/login/", methods=["POST"])
def login():
    response = {}

    if request.method == "POST":

        username = request.json['username']
        password = request.json['password']

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


# View users
@app.route('/get-user/<username>/')
def get_user(username):
    response = {}

    with sqlite3.connect('point_of_sale.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user where username={}'.format(username))

        response['status_code'] = 200
        response['message'] = 'User retrieved successfully'
        response['user'] = cursor.fetchone()

    return response


@app.route('/edit-profile/<int:user_id>', methods=['PUT'])
def edit_profile(user_id):
    response = None

    if request.method == 'PUT':
        incoming_data = dict(request.json)
        db = Database()
        response = db.edit_profile(incoming_data, user_id)

        return response


# Trolley & Products
# Adding a product
@app.route('/adding/', methods=["POST"])
@jwt_required()
def add_products():
    response = {}

    if request.method == "POST":
        category = request.form['category']
        name = request.form["name"]
        price = request.form['price']
        description = request.form['description']

        with sqlite3.connect("point_of_sale.db") as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO product("
                           "category,"
                           "name,"
                           "price,"
                           "description) VALUES(?, ?, ?, ?)", (category, name, price, description))
            connection.commit()
            response["message"] = "success"
            response["status_code"] = 201
        return response


# View products
@app.route('/view/')
def view_products():
    response = {}

    with sqlite3.connect("point_of_sale.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM product")

        products = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = products
    return response


# Viewing 1 product individually
@app.route('/view-one/<int:product_id>/')
def view_one_product(product_id):
    response = {}

    with sqlite3.connect("point_of_sale.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM product WHERE product_id=?", str(product_id))
        product = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = product
    return response


# Edit a product and targeting the product's specific id
@app.route('/changing/<int:product_id>/', methods=["PUT"])
@jwt_required()
def updating_products(product_id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('point_of_sale.db') as conn:
            print(request.json)
            incoming_data = dict(request.json)
            put_data = {}

            if incoming_data.get("category") is not None:
                put_data["category"] = incoming_data.get("category")

                with sqlite3.connect('point_of_sale.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute("UPDATE product SET category =? WHERE product_id=?", (put_data["category"],
                                                                                         product_id))
            elif incoming_data.get("name") is not None:
                put_data["name"] = incoming_data.get("name")

                with sqlite3.connect('point_of_sale.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute("UPDATE product SET name =? WHERE product_id=?",
                                   (put_data["name"], product_id))

                    conn.commit()
                    response['message'] = "Update was successfully"
                    response['status_code'] = 200

    return response


# Deleting a product and target a specific product id
@app.route('/delete/<int:product_id>/')
@jwt_required()
def delete_products(product_id):
    response = {}

    with sqlite3.connect("point_of_sale.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM product WHERE product_id=" + str(product_id))
        connection.commit()
        response['status_code'] = 200
        response['message'] = "Product deleted successfully."
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()
