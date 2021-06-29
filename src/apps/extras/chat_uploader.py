import streamlit as st
from pathlib import Path
import os
from io import StringIO
from config import TMP_DIR, CHAT_PATH
from .chat_parser import chat_parser
import pandas as pd
import numpy as np
import time
import pickle
from utils import refresh_page

from utils import save_chat, read_chat, delete_chat

def chat_uploader():
    if os.path.exists(CHAT_PATH):
        chat, file_name = read_chat(return_name=True)
        st.markdown('''<style>
        section.main > div.block-container > div > div > div.stMarkdown > div > p {
                    text-align: center;
                }
        </style>''', unsafe_allow_html=True)
        names = chat['name'].unique()
        st.markdown(f'''לבין `{names[1]}` `{names[0]}` שיחות בין''')
        min_date = chat['datetime'].dt.date.min()
        max_date = chat['datetime'].dt.date.max()
        st.markdown(f'''`{min_date}` בין התאריכים `{max_date}` לבין''')
        st.markdown(f'''`{file_name}` :הקובץ''')
        st.write(chat.head())
        if st.button('העלה מחדש'):
            delete_chat()
            time.sleep(1)
            refresh_page()  
            return None
        return chat
    chat = None
    uploaded_file = st.file_uploader('', type = 'txt')
    if uploaded_file is not None:
        file_name = uploaded_file.name
        if st.button('שמור'):
            f = StringIO(uploaded_file.getvalue().decode("utf-8"))
            lines = f.readlines()
            chat = chat_parser(lines)

            chat_dict = {
                'df': chat,
                'name': file_name
            }
            save_chat(chat_dict)
            time.sleep(1)
            refresh_page()
    return chat