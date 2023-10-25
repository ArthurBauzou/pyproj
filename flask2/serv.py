from flask import Flask, render_template, jsonify, request

from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker

from model.model import Customer, Product

app = Flask(__name__)
app.testing = True
app.config.update({
    "TESTING": True,
    "TEMPLATES_AUTO_RELOAD": True
})

engine = create_engine('mysql+pymysql://root:root@localhost:3306/tmpdb')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customers', methods=['GET'])
def get_users():
    if 'id' in request.args:
        r_id = int(request.args['id'])
        select = session.query(Customer).filter(Customer.id == r_id)
    else :
        select = session.query(Customer).all()
    response = []
    for r in select : 
        row = r.__dict__
        del(row['_sa_instance_state'])
        response.append(row)
    return jsonify(response), 200

@app.route('/customers/<name>', methods=['GET'])
def get_user(name):
    select = session.query(
        Customer.firstname,
        Customer.lastname
        ).filter(Customer.firstname == name).first()
    if select is None : 
        return 'Pas encore inscit !?!?!?!?!? (wtf)'
    else :
        return render_template('pageperso.html', data = select), 200

@app.route('/products', methods=['GET'])
def get_products():
    if 'id' in request.args:
        r_id = int(request.args['id'])
        select = session.query(Product).filter(Product.id == r_id)
    else :
        select = session.query(Product).all()
    response = []
    for r in select : 
        row = r.__dict__
        del(row['_sa_instance_state'])
        response.append(row)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

session.close()