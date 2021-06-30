import streamlit as st

from .extras.chat_uploader import chat_uploader
from .extras.chat_parser import chat_parser



def app():
    st.title('העלאת קובץ שיחה')

    st.markdown(f'''<p style='text-align: right'>
     ניתן לייצא את קובץ השיחה ע"י
    <a href = 'https://faq.whatsapp.com/android/chats/how-to-save-your-chat-history/?lang=he'>מדריך גיבוי וואטסאפ</a>
     תחת יצוא היסטוריית הצ‘אט
    </p>''', unsafe_allow_html=True)

    chat_uploader()

