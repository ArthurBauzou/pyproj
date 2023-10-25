from sqlalchemy import func, create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker

import json, datetime
import pandas as pd

from model.model import Customer, Product, Order, Purchase, Schema

def bk(n=4, text:str=None):
    if text :
        line = ' '.join([n*'–', f'{text.upper()}', n*'–'])
    else :
        line = n*'–'
    print('\n', line)

# création du moteur avec les coordonées de la base de données
url = f'mysql+pymysql://root:root@localhost:3306/tmpdb'
# engine = create_engine(url, echo=True)
engine = create_engine(url)

# au cas ou on drop tous ce qui existe
if database_exists(engine.url):
    drop_database(engine.url)
    print('droppped ! ')

# création de la base puis des tables
create_database(engine.url)
Schema.metadata.create_all(engine)

# Création de la session
Session = sessionmaker(bind=engine)
session = Session()


# enfin on insère dans la table client et produit
with open('./datas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for c in data['customers']:
    new_customer = Customer(**c)
    session.add(new_customer)
for p in data['products']:
    new_product = Product(**p)
    session.add(new_product)

# création de commande : 
for c in data['orders']:
    curr_date = datetime.datetime.now()
    new_order = Order(
        date=curr_date,
        customer_id = c['customer']
    )
    session.add(new_order)
    session.flush()
    session.refresh(new_order)
    print(f'commande n° {new_order.id} créée')
    #création des achats dans la commande
    for p in c['purchases'] :
        new_purchase = Purchase(
            product_id = p[0],
            order_id = new_order.id,
            quantity = p[1]
        )
        session.add(new_purchase)

session.commit()

# vérifions avec des requêtes
# afficher les infos dea utilisateurs dans un tuple
bk(3,'liste des clients')
for c in session.query(
    Customer.firstname,
    Customer.lastname,
    Customer.id.label('Numéro client')
    ).all():
    print(c)

# compter le nombre de produits et d’achats
bk()
print('nombre de produits : ',session.query(Product.id).count())
print('nombre d’ achats : ',session.query(Purchase.order_id).count())

# afficher les achats avec détails dans un tableau :
bk(3, 'liste enrichie des achats')
achats = session.query(
    Purchase.quantity,
    Product.name,
    Customer.firstname,
    Customer.lastname,
    Order.id,
    Order.date
).join(
    Product, Purchase.product_id == Product.id
).join(
    Order, Purchase.order_id == Order.id
).join(
    Customer, Order.customer_id == Customer.id
).all()

a_res = [[
    x[1], 
    x[0], 
    x[2]+' '+x[3],
    x[4],
    x[5].strftime('%H:%M:%S'),
    x[5].strftime('%Y-%m-%d')
    ] for x in achats]
df_a = pd.DataFrame(a_res, columns=['produit', 'quantité', 'acheteur', 'N° de commande', 'heure', 'date'])
print(df_a)

# affiche le total coût des commandes
bk(3, 'prix des commandes')
commandes = session.query(
    func.sum(Purchase.quantity*Product.price),
    Customer.lastname,
    Customer.firstname,
    Order.id
).join(
    Product, Purchase.product_id == Product.id
).join(
    Order, Purchase.order_id == Order.id
).join(
    Customer, Order.customer_id == Customer.id
).group_by(Order.id).all()

c_res = [[
    x[3],
    x[2]+' '+x[1],
    f'{round(x[0], 2)} €'
] for x in commandes]

df_c = pd.DataFrame(c_res, columns=['N° de commande', 'Nom du client', 'Total'])
print(df_c)

# test de suppression d’une commande > entraine la suppresion des achats associés
bk(3, 'test de suppression en cascade')
order_to_del = session.query(Order).filter(Order.id == 3).first()
if order_to_del : session.delete(order_to_del)
session.commit()
#verif : 
print('nombre d’ achats après suppression de la commande 3 : ',session.query(Purchase.order_id).count())


session.close()