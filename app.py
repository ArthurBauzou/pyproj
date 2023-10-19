import components.victimes as vic
import components.projectiles as proj
import random as rd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

#––– FONCTIONS–––#

def throw_at(victim:vic.Victim, object:proj.Projectile, speed=-1):
    object.throw(speed)
    st.write(
        f'{object.name} a été jetté sur {victim.name} avec une force de {object.get_force()}'
        )
    msg, scr = victim.hit(object.get_pain())
    st.write(msg)
    if scr : 
        scr = f'''
        <p style="
            font-size: 24px;
            color: orange;
        "> {scr}
        '''
        st.write(scr, unsafe_allow_html=True)
    object.speed = 0
    st.write('–––––––')

def sinusoid(f, T=0.01, ech=40000):
    x = np.arange(0, T, 1/ech)
    y = np.sin(np.pi*2*f*x)

    return x, y

#––––––––––––––––––––––#
#––– PAGE STREAMLIT –––#
#––––––––––––––––––––––#

#––– EN-TÊTE –––#

st.title('Le jette-o-matic')
st.image('https://i.imgur.com/DoWlYF6.jpeg', width=256)
st.write('Ici on jette des trucs sur des gens jusqu’a ce qu’ils crient, mais dans le respect')

#––– COLONNES DES ENTITÉS –––#

col1, col2 = st.columns(2)

with col1:
    st.header('VICTIMES')
    v_textboxes = []
    victims:list[vic.Victim] = []
    for i,n in enumerate([
        'Emma',
        'Lucas',
        'Sofia',
        'Thomas'
    ]):
        v_textboxes.append( st.text_input(
            label = f'vn{i}', 
            value = n, 
            label_visibility = 'hidden'
            ))
        victims.append(vic.Victim(v_textboxes[i]))

    if st.checkbox('voir '):
        vic_df = pd.DataFrame([
            [v.name, v.tolerance, v.scream(8)] for v in victims]
            ,columns=['nom', 'tolérance', 'cri'])
        st.table(vic_df)

with col2:
    st.header('PROJECTILES')
    o_textboxes = []
    projectiles:list[proj.Projectile] = []
    for i, o in enumerate([
        'un Rouleau-Compresseur',
        'une Assiette',
        'un Ours en Peluche',
        'une Hache'
    ]):
        o_textboxes.append(st.text_input(
            label = f'on{i}', 
            value = o, 
            label_visibility = 'hidden'
            ))
        projectiles.append(proj.Projectile(o_textboxes[i]))
        
    if  st.checkbox('voir'):
        obj_df = pd.DataFrame([
            [o.name, o.weight, o.firmness] for o in projectiles],
            columns=['type', 'poids', 'dureté'])
        st.table(obj_df)

rd.shuffle(victims)
rd.shuffle(projectiles)

#––– COMMANDES –––#

force_slider = st.slider('vitesse', 0.2, 5.0, 2.0, 0.2)

throw_button = st.button('LAN-CE-MENT')

if throw_button : 
    for o,v in zip(projectiles, victims):
        throw_at(v, o, force_slider)

freq_slider = st.slider('fréquence', 80, 800, 440, 1)

#––– SINUSOIDE –––#

fig, ax = plt.subplots()
s_x, s_y = sinusoid(freq_slider)
ax.plot(s_x, s_y)
# st.pyplot(fig)
st.line_chart(s_y)

