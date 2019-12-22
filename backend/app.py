from flask import Flask, request, logging, jsonify
from flask_mysqldb import MySQL
from haversine import haversine
from decimal import Decimal
import json
import numpy as np
from datetime import datetime
import time


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
        return "post HELLO"
    return {}


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
        result = cursor.execute("SELECT  * from users where username=%s", [usernamegot])
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
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    user_id = request.form["user_id"]
    timestamp = request.form["timestamp"]
    # mysql execution
    cursor = mysql.connection.cursor()
    statement = "UPDATE helpers set latitude={0},longitude={1},location_timestamp='{2}' WHERE user_id={3}".format(
        latitude, longitude, timestamp, user_id
    )
    print("[log]:  " + statement)
    if cursor.execute(statement):
        mysql.connection.commit()
        return {"message": "success"}
    else:
        return {"message": "failure"}
    cursor.close()


@app.route("/distress", methods=["POST"])
def distress():
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    user_id = request.form["user_id"]
    timestamp = request.form["timestamp"]

    user_location = (Decimal(latitude), Decimal(longitude))
    cur_ts = datetime.timestamp(datetime.now())
    # mysql execution
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO situations (user_id,situation_timestamp,latitude,longitude) VALUES ({0},'{1}',{2},{3})".format(
            user_id, timestamp, latitude, longitude
        )
    )
    mysql.connection.commit()
    result = cursor.execute("SELECT * FROM  helpers")
    helpers = cursor.fetchall()
    out_json = []

    for helper in helpers:
        helper_location = (Decimal(helper["latitude"]), Decimal(helper["longitude"]))

        dis = haversine(user_location, helper_location)
        print("distance:{0}".format(dis))

        timestamp_str = helper["location_timestamp"]
        str_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        time_sec = time.mktime(str_timestamp.timetuple())

        if dis < 10 and cur_ts - time_sec <= 20:
            helper_object = {
                "helper_id": helper["user_id"],
                "name": helper["name"],
                "latitude": str(helper["latitude"]),
                "longitude": str(helper["longitude"]),
            }
            out_json.append(helper_object)
    cursor.close()
    return jsonify([j for j in out_json])


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
