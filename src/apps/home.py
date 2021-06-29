import streamlit as st

from .extras.chat_uploader import chat_uploader
from .extras.chat_parser import chat_parser



def app():
    st.title('העלאת קובץ שיחה')

    st.markdown(f'''<p style='text-align: right'>
    ....ניתן להוריד את השיחה ע"י
    </p>''', unsafe_allow_html=True)
    
    chat_uploader()

