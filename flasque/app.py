from flask import Flask
from flask import render_template
from pymongo import MongoClient, errors

app = Flask(__name__)
app.testing = True
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)

#––– SGBD –––#
client = MongoClient("mongodb://localhost:27017/")
db = client.colorDB

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

@app.route('/users')
def get_users():
    total_users = db.users.find()
    return render_template('users.html',
                           users = total_users
    )