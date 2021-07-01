import streamlit as st
import numpy as np
import pandas as pd
from utils import is_chat_exist, read_chat


def get_real_conversation(chat):
    dates = chat['datetime'].dt.date
    massages_per_date = chat.groupby(dates)['text'].count()
    valid_dates = massages_per_date[massages_per_date > 10].index
    if len(valid_dates) == 0:
        valid_dates = dates

    chosen_date = np.random.choice(valid_dates)
    chat_at_date = chat[dates == chosen_date]
    title = f'{chosen_date} :שיחה בתאריך'
    return chat_at_date, title

def display_random_conversation():
    chat = read_chat()

    semi_chat, title = get_real_conversation(chat)

    names = chat['name'].unique()
    right_idx = np.where(semi_chat['name'] == names[0])[0]

    st.title(title)
    import time
    html = ''
    for idx in right_idx:
        html += """
                div:nth-child(""" + str(8 + idx) + """) > div.stMarkdown > div > p {
                float:left;
                text-align: left;
                }
            """
    st.markdown(f"""
        <style>
        {html}
        </style>""", unsafe_allow_html=True)
    for _, massage in semi_chat.iterrows():
        # if i % 2 == 0:
        #     float_css = 'right'
        # else:
        #     float_css = 'left'
        # /**/
        st.write(massage['name'] + ": `" + massage['text'] + '`')
        time.sleep(1)


def app():
    st.title('ייצר שיחה')

    if not is_chat_exist():
        st.write('!העלה קובץ בדף הראשי')
        return

    display_random_conversation()



