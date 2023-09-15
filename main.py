import random
import time

import requests
import streamlit as st
from streamlit_javascript import st_javascript as st_js
from streamlit.components.v1 import html
from validate_email import validate_email


def send_message(message):
    if len(message) > 0:
        response = requests.post(
            'http://127.0.0.1:8000/send_message',
            data={
                'message': message,
                'token': st.experimental_get_query_params()['token'],
            }
        )

        print(response.json())

    else:
        st.toast('Tu dois écrire un message')


def set_sign_in():
    st.session_state['sign_in'] = True
    if 'sign_up' in st.session_state:
        del st.session_state['sign_up']


def set_sign_up():
    st.session_state['sign_up'] = True
    if 'sign_in' in st.session_state:
        del st.session_state['sign_in']


def sign_in(data):
    if len(data) == 2:
        if not validate_email(data[0]):
            st.toast('Adresse email invalide')

        elif len(data[1]) < 8:
            st.toast('Mot de passe trop court')

        else:
            response = requests.post(
                'http://127.0.0.1:8000/login',
                data={
                    'email': data[0],
                    'password': data[1],
                }
            )

            del st.session_state['sign_in']
            print(response.json()['code'])
            if response.json()['code'] == 101:
                st.toast('Mot de passe incorrect')
                st.session_state['sign_in'] = True

            elif response.json()['code'] == 100:
                st.experimental_set_query_params(token=response.json()['token'])
                st.toast('connected successful')
                time.sleep(1)
                st.session_state['connected'] = True

            elif response.json()['code'] == 102:
                st.toast('Une erreur est  survenue, il faut réessayer')
                st.session_state['sign_in'] = True

    else:
        st.toast('Tu dois remplir les champs')


def sign_up(data):
    if len(data) == 3:
        if not validate_email(data[0]):
            st.toast('Adresse email invalide')

        elif data[1] != data[2]:
            st.toast('Les deux mots de passe sont différents')

        elif len(data[1]) < 8:
            st.toast('Mot de passe trop court')

        else:
            response = requests.post(
                'http://127.0.0.1:8000/create_account',
                data={
                    'email': data[0],
                    'password': data[1],
                }
            )

            del st.session_state['sign_up']

            if response.json()['code'] == 101:
                st.session_state['sign_in'] = True

            elif response.json()['code'] == 100:
                st.experimental_set_query_params(token=response.json()['token'])
                st.toast('connected successful')
                time.sleep(1)
                st.session_state['connected'] = True

            elif response.json()['code'] == 102:
                st.toast('Une erreur est  survenue, il faut réessayer')

    else:
        st.toast('Tu dois remplir les champs')


def main():
    if 'sign_in' in st.session_state:
        st.title('Dialogflow/_connexion')
        email = st.text_input('Adresse email', key="4")
        password = st.text_input('Mot de passe', key="5")

        data = []
        for i in [email, password]:
            if len(i) > 0:
                data.append(i)

        st.button('se connecter', on_click=sign_in, args=(data,))

    elif 'sign_up' in st.session_state:
        st.title('Dialogflow/_création_de_compte')
        email = st.text_input('Adresse email', key="2")
        password = st.text_input('Mot de passe', key="1")
        repeat_password = st.text_input('Répéter le mot de passe', key="3")

        data = []
        for i in [email, password, repeat_password]:
            if len(i) > 0:
                data.append(i)

        st.button('créer un compte', on_click=sign_up, args=(data,))

    elif 'connected' in st.session_state or 'token' in st.experimental_get_query_params():
        st.session_state['connected'] = True
        chat_input = st.chat_input()

        if chat_input:
            send_message(chat_input)

        # get history
        response = requests.get(
            'http://127.0.0.1:8000/get_history',
            data={
                'token': st.experimental_get_query_params()['token'],
            }
        )

        if response.json()["code"] == 100:
            history = response.json()["history"]

            for i in history:
                with st.chat_message(i["role"]):
                    st.markdown(i["content"])

        with st.chat_message('ai'):
            st.button('CLEAR CHAT')

    else:
        print(st.session_state)
        st.title('Dialogflow')
        st.button('Connexion', on_click=set_sign_in)
        st.button('Création de compte', on_click=set_sign_up)


if __name__ == '__main__':
    main()
