import streamlit as st
import pandas as pd
import random as rd
from pymongo import MongoClient, errors

from userclass import User

def give_bg_color(color, text):
    return f'''
        <p style="
            background-color: {color};
            font-size: 24px;
            color: white;
            padding: 14.75px;
            border-radius: 4px;
            text-align: center;
        "> {text} </p>
        '''

def make_grad(list, pos, value):
    pass

tab1, tab2, tab3 = st.tabs(['degradé', 'random', 'palette'])

with tab1:
    st.header('Génération d’un dégradé')

    col1, col2 = st.columns([1,3])

    with col1 : 
        col_input = []
        for i,c in enumerate([
            "#6c5e53", 
            "#917546", 
            "#97b9e0", 
            "#7fc3e1", 
            "#e6ddca", 
            "#e7c084"
        ]):
            col_input.append( st.text_input(
            label = f'color{i}', 
            value = c, 
            label_visibility = 'hidden'
            ))

    with col2 : 
        for i,c in enumerate(col_input):
            kaomojis = [
                '(╬▔皿▔)╯',
                '(*￣3￣)╭',
                'ヾ(•ω•`)o',
                'o(*°▽°*)o',
                '( •̀ ω •́ )✧',
                'q(≧▽≦q)',
                '(´。＿。｀)',
                '(╯°□°）╯︵ ┻━┻',
                '(⊙_⊙)？',
                '(ﾉ*･ω･)ﾉ'
            ]
            color_name = rd.choice(kaomojis)
            st.write(give_bg_color(c, color_name), unsafe_allow_html=True)

with tab2:
    st.header('Random colors from file')
    color_list = []

    file_type = st.radio('type de fichier',
                         ['JSON', 'Excel', 'CSV'],
                         horizontal=True)
    if file_type == 'CSV':
        file = st.file_uploader('importez un fichier CSV : ', type='csv')
        if file : 
            dfc = pd.read_csv(file)
            biglist = dfc['hex'].to_list()
            color_list = rd.sample(biglist, 6)

            for i,c in enumerate(color_list):
                color_name = dfc.loc[dfc['hex']==c]['name'].to_string()
                st.write(give_bg_color(c, color_name), unsafe_allow_html=True)

            st.write(color_list)
            st.write(dfc.head())

    else :
        st.write('déso mais c’est pas encore possible 😔')
        file = None

with tab3:
    st.header('Test base de données')
    client = MongoClient("mongodb://localhost:27017/")
    db = client.colorDB
    users = db.users
    users.create_index('username', unique=True)

    n_username = st.empty()
    n_pwd = st.empty()
    n_email = st.empty()

    nu = n_username.text_input('username', value='')
    np = n_pwd.text_input('password', value='')
    ne = n_email.text_input('email', value='')

    if nu and np and ne :
        new_user = User(nu, np, ne)
        valid = new_user.get_validation()
        if all(v == True for v in valid.values()) :
            submit = st.button('submit', disabled=False)
        else : 
            for v in valid.values():
                if type(v) == str : st.write(f':red[{v}]')
            submit = st.button('submit', disabled=True)
    else : 
        submit = st.button('submit', disabled=True)

    if submit :
        try:
            users.insert_one({
                'username': new_user.username,
                'password': new_user.password,
                'email': new_user.email,
                'since': new_user.since
            })
        except errors.DuplicateKeyError:
            st.write(f':red[{new_user.username} existe déjà dans la base]')
        else :
            st.write(f'merci de vous être inscrit, {new_user.username} !')
            # hack pour reset les champs
            n_username.text_input('username', value='', key=2)
            n_email.text_input('email', value='', key=3)
            n_pwd.text_input('password', value='', key=4)

    usertable = []
    for u in users.find():
        usertable.append([u['username'], u['email'], u['since']])
    
    user_df = pd.DataFrame(usertable, columns=['nom', 'e-mail', 'inscrit le'])
    st.table(user_df)
