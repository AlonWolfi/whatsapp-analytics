import streamlit as st

from utils import read_chat

import os
import time
from config import DATA_DIR
from utils import read_data, save_data

def get_sentence_start(file_path = DATA_DIR / 'tmp' / 'sentence_start.txt'):
    sentence_start = 'בוקר טוב'
    if os.path.exists(file_path):
        sentence_start = read_data(file_path)
    text_input = st.text_input(label='תחילת משפט', value=sentence_start)
    if text_input != sentence_start:
        save_data(text_input, file_path)
        sentence_start = text_input
        time.sleep(2)
    return sentence_start



def app():

    sentence_start = get_sentence_start()

    st.markdown("""
        <style>
        label {
            text-align: right;
        }
        </style>""", unsafe_allow_html=True)
    from .modeling.predict import complete_sentence
    answers = complete_sentence(sentence_start)
    name = read_chat()['name'].unique()[1]
    for i, answer in enumerate(answers):
        st.write(name + ": `" + answer + '`')
