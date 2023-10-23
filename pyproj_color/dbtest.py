from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.colorDB
users = db.users
# users.drop()
users.create_index('username', unique=True)

users.insert_one({
    'username': 'arthur',
    'password': 'password',
    'email': 'arthurbauzou@gmail.com',
    'since': 'forever'
})

for u in users.find():
    print(u)