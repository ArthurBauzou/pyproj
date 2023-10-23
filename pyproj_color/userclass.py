import datetime
import re

class User:
    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = password
        self.email = email
        now = datetime.datetime.now()
        self.since = now.strftime("%d/%m/%Y %H:%M:%S")
        self.valid_feilds = {}
        self.validate()

    def validate(self):
        #––– USERNAME –––#
        if len(self.username) >= 4:
            self.valid_feilds['username'] = True
        else :
            self.valid_feilds['username'] = 'Votre nom doit comporter au moins 4 carractères'
        
        #––– EMAIL –––#
        email_pattern = re.compile(r'[\w+-]*@[\w+-]*\.[a-z0-9]*')
        if email_pattern.match(self.email):
            self.valid_feilds['email'] = True
        else : 
            self.valid_feilds['email'] = 'Entrez un email valide'

        #––– PASSWORD –––#
        if len(self.password) >= 8:
            self.valid_feilds['password'] = True
        else :
            self.valid_feilds['password'] = 'Votre mot de passe doit comporter au moins 8 carractères'

    def get_validation(self):
        return self.valid_feilds


#TEST
# peter = User('peter', 'WXCSR', 'truc@gmail.com')

# val = peter.get_validation()
# for k,v in val.items():
#     print(k,v)

# print(peter.since)