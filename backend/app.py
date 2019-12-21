from flask import Flask, request, logging
from flask_mysqldb import MySQL
from haversine import haversine

# from passlib.hash import sha256_crypt
# from functools import wraps
import logging

# starting a flask app
app = Flask(__name__)
app.secret_key = "secretpragyan"

# flask-mysql database connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "pragyan_hack"
app.config["MYSQL_PASSWORD"] = "Pragyan_hack123"
app.config["MYSQL_DB"] = "pragyan_hack"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
# mysql initialization
mysql = MySQL(app)

# index route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # app.logger("inside")
        return "post HELLO"
    return "get hello"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usernamegot = request.form["user"]
        passwordgot = request.form["pass"]
        output = "failure"
        is_helper = False
        user_id = 0
        # mysql connection
        cursor = mysql.connection.cursor()
        result = cursor.execute(
            "SELECT  * from users where username=%s",[usernamegot]
        )
        if result > 0:
            data = cursor.fetchone()
            password = str(data["password"])
            user_id = data["user_id"]
            if password == passwordgot:
                output = "success"
                helper_result = cursor.execute(
                    "SELECT * from helpers where user_id=%s", [user_id]
                )
                if helper_result > 0:
                    is_helper = True

        cursor.close()
        return {"message": output, "user_id": user_id, "is_helper": is_helper}
    else:
        return "You are not supposed to be here: You have registered to be hacked by your activity"


@app.route("/location_update", methods=["POST"])
def location_update():
    lattitude = request.form["lattitude"]
    longitude = request.form["longitude"]
    user_id = request.form["user_id"]
    # mysql execution


@app.route("/distress", methods=["POST"])
def distress():
    lattitude = request.form["lattitude"]
    longitude = request.form["longitude"]
    user_location = (lattitude, longitude)
    # mysql execution
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM  helpers")
    helpers = cursor.fetchall()
    out_json = []
    for helper in helpers:
        if haversine(user_location, (helper.lattitude, helper.longitude)) < 0.5:
            helper_object = {
                id: helper.id,
                name: helper.name,
                lattitude: helper.lattitude,
                longitude: helper.longitude,
            }
            out_json.append(helper_object)
    cursor.close()
    return out_json


@app.route("/situation_messages", methods=["POST"])
def assist():
    user = request.form["user"]
    user_id = request.form["user_id"]
    # base_amplitude = request.form["base_amplitude"]
    current_amplitude = request.form["current_amplitude"]
    lattitude = request.form["lattitude"]
    longitude = request.form["longitude"]
    msg = request.form["msg"]
    return msg


if __name__ == "__main__":
    # app.run()
    # app.run(debug=True,host='0.0.0.0',port="12345")
    app.run(debug=True, port=7000)
