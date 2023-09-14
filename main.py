import random
import time

import streamlit as st

from validate_email import validate_email


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
            try:
                del st.session_state['sign_in']
                del st.session_state['sign_up']

            except:
                pass

            time.sleep(2)
            st.session_state['connected'] = True
    else:
        st.toast('Tu dois remplir les champs')


def sign_up():
    pass


def main():
    if 'sign_in' in st.session_state:
        st.title('Dialogflow/_connexion')
        email = st.text_input('Adresse email')
        password = st.text_input('Mot de passe')

        data = []
        for i in [email, password]:
            if len(i) > 0:
                data.append(i)

        st.button('se connecter', on_click=sign_in, args=(data,))

    elif 'sign_up' in st.session_state:
        st.title('Dialogflow/_création_de_compte')
        st.text_input('Adresse email')
        st.text_input('Mot de passe')
        st.text_input('Répéter le mot de passe')
        st.button('créer un compte')

    elif 'connected' in st.session_state:
        chat_input = st.chat_input()
        st.button('connect')
        st.button('Vider le chat')
        a = st.chat_message('user')
        b = st.chat_message('assistant')

        for i in range(100):
            with st.chat_message(random.choice(["user", "assistant"])):
                st.write(i)

        with st.chat_message('assistant'):
            st.button('CLEAR CHAT')

    else:
        st.title('Dialogflow')
        st.button('Connexion', on_click=set_sign_in)
        st.button('Création de compte', on_click=set_sign_up)


if __name__ == '__main__':
    main()
