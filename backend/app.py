from flask import Flask, request
from flask_mysqldb import MySQL

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
        app.logger("inside")
        return "post HELLO"
    return "get hello"


if __name__ == "__main__":
    # app.run()
    # app.run(debug=True,host='0.0.0.0',port="12345")
    app.run(debug=True, port=7000)
