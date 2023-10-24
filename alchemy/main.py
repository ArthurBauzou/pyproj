from sqlalchemy import URL, create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
import json

from model.model import Customer, Product, Order, Purchase, Schema

url = f'mysql+pymysql://root:root@localhost:3306/tmpdb'

engine = create_engine(url, echo=True)

if database_exists(engine.url):
    drop_database(engine.url)
    print('droppped ! ')

create_database(engine.url)

with open('./datas.json', 'r') as f:
    data = json.load(f)
    print(data['customers'][0])