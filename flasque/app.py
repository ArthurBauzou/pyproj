from flask import Flask
from flask import render_template

app = Flask(__name__)

user_props = {
    'username': '',
    'password': '',
    'email': ''
}

@app.route('/')
def home():
    return render_template('home.html',
        user = user_props
    )