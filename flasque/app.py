from flask import Flask
from flask import render_template
from pymongo import MongoClient, errors

app = Flask(__name__)

#––– SGBD –––#
client = MongoClient("mongodb://localhost:27017/")
db = client.colorDB
users = db.users

user_props = {
    'username': '',
    'password': '',
    'email': ''
}

#––– ROUTES –––#
@app.route('/')
def home():
    return render_template('home.html',
        user = user_props.keys()
    )