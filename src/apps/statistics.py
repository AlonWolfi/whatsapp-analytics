import re
import string

import emoji
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

from apps.extras.hebrew_stopwords import hebrew_stopwords, hebrew_alphabet
from config import DATA_DIR
from utils import is_chat_exist, read_chat

MEDIA_TOKEN = '<M>'
URL_TOKEN = '<url>'
TOKENS = [MEDIA_TOKEN, URL_TOKEN]


def preprocess_text_for_wordcloud(text):
    text = re.sub('<המדיה לא נכללה>', MEDIA_TOKEN, text)
    text = re.sub('https?://\S+|www\.\S+', URL_TOKEN, text)
    return text


def reverse_text(text):
    return text[::-1]


def extract_emojis(text):
    return ''.join([c for c in text if (c.lower() not in '<>אבגדהוזחטיכךלמםנןסעפףצץקרשתabcdefghijklmnopqrstuzwxyz')])


@st.cache
def get_text_for_name(chat, name):
    text = chat[chat['name'] == name]['text']
    return text.apply(preprocess_text_for_wordcloud)


@st.cache
def get_emojis_for_name(chat, name):
    emojis = list(emoji.UNICODE_EMOJI['en'].keys())

    def extract_emojis(text):
        return ''.join([c for c in text if c in emojis])

    text = chat[chat['name'] == name]['text']
    return text.apply(extract_emojis)


@st.cache
def generate_wordcloud(text_series):
    text = ' '.join(text_series.apply(reverse_text))
    emoji_unicodes = list(emoji.UNICODE_EMOJI['en'].keys())
    stopwords = hebrew_stopwords + hebrew_alphabet + emoji_unicodes + [t[1:-1] for t in TOKENS]
    stopwords = [reverse_text(word) for word in stopwords]
    wc = WordCloud(background_color="#f1f1f1", stopwords=stopwords, font_path=str(DATA_DIR / 'fonts' / 'arial.ttf'),
                   min_word_length=2).generate(text).recolor(colormap='tab10')
    return wc


@st.cache
def generate_emojicloud(text_series):
    text = ' '.join(text_series.apply(extract_emojis))

    normal_word = r"(?:\w[\w']+)"
    # 2+ consecutive punctuations, e.x. :)
    ascii_art = r"(?:[{punctuation}][{punctuation}]+)".format(punctuation=string.punctuation)
    # a single character that is not alpha_numeric or other ascii printable
    emoji_re = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)
    regexp = r"{normal_word}|{ascii_art}|{emoji}".format(normal_word=normal_word, ascii_art=ascii_art,
                                                         emoji=emoji_re)

    wc = WordCloud(background_color="#f1f1f1", font_path=str(DATA_DIR / 'fonts' / 'Symbola.ttf'),
                   regexp=regexp).generate(text).recolor(colormap='tab10')
    return wc


def display_cloud(wc, with_streamlit=True):
    fig, axs = plt.subplots(facecolor="#f1f1f1")
    axs.imshow(wc, interpolation='bilinear')
    axs.axis("off")
    plt.tight_layout(pad=0)
    if with_streamlit:
        st.pyplot(fig)
    else:
        plt.show()


def do_for_all_names(names, func_for_name, title: str = None):
    cols = st.beta_columns(len(names))
    for idx, name in enumerate(names):
        with cols[idx]:
            if title:
                st.write(title if idx == 1 else '‎‎‎‎‎‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎')
            func_for_name(name)


def _title_name(name):
    st.title(name)


def _display_wordcloud_name(text):
    wc = generate_wordcloud(text)
    display_cloud(wc)


def _display_emojicloud_name(text):
    ec = generate_emojicloud(text)
    display_cloud(ec)


@st.cache
def average_massage(text, substr):
    count = text.str.contains(substr).sum()
    return np.round(len(text) / count)


def _display_average_massage(text, substr):
    am_len = average_massage(text, substr)
    if len(substr) > 1:
        substr = f"""<i>{substr}</i>"""
    if am_len != np.inf:
        st.markdown(f"""שולח/ת '{substr}' כל `{int(am_len)}` הודעות""", unsafe_allow_html=True)
    else:
        st.markdown(f"""שולח/ת '{substr}' אף פעם""", unsafe_allow_html=True)


def _display_average_emoji(text):
    ae_len = average_massage(text, '[' + ''.join(list(emoji.UNICODE_EMOJI['en'].keys())) + ']')
    st.markdown(f"""שולח/ת אמוג'י כל `{int(ae_len)}` הודעות""", unsafe_allow_html=True)


@st.cache
def tokenize_text(text):
    return text.str.split(' ')


def max_massage_len(text):
    return max(tokenize_text(text).apply(len))


def _display_max_massage_len(text):
    st.markdown(f"""ההודעה הארוכה ביותר: `{int(max_massage_len(text))}` מילים!""", unsafe_allow_html=True)


def massage_len_hist(text):
    series = tokenize_text(text).apply(len)
    series = series[series < np.quantile(series, 0.996)]
    # hist = np.histogram(series, bins = 50, range = (0,np.quantile(series,0.998)))
    return series


def _display_massage_len_hist(txt_dict, names):
    import plotly.figure_factory as ff
    hist_data = [massage_len_hist(txt_dict[name]) for name in names]
    group_labels = names
    fig = ff.create_distplot(hist_data, group_labels)
    fig.update_layout(paper_bgcolor="#f1f1f1")
    fig.update_layout(plot_bgcolor="#f1f1f1")
    st.plotly_chart(fig, use_container_width=True)


def first_massage(chat, name):
    first_massage_by_date = chat.groupby(chat['datetime'].dt.date).first()['name']
    fm_vc = first_massage_by_date.value_counts() / len(first_massage_by_date)
    return np.round(fm_vc[name], 2)


def first_boker(chat, name):
    chat = chat[chat['text'].str.contains('בוקר')]
    first_massage_by_date = chat.groupby(chat['datetime'].dt.date).first()['name']
    fm_vc = first_massage_by_date.value_counts() / len(first_massage_by_date)
    return np.round(fm_vc[name], 2)


def first_night(chat, name):
    chat = chat[chat['text'].str.contains('לילה')]
    first_massage_by_date = chat.groupby(chat['datetime'].dt.date).first()['name']
    fm_vc = first_massage_by_date.value_counts() / len(first_massage_by_date)
    return np.round(fm_vc[name], 2)


def _display_first_massage(chat, name):
    fm = first_massage(chat, name)
    fm = str(int(fm * 100)) + '%'
    st.markdown(f"""כותב/ת הודעה ראשונה `{fm}` מהפעמים""", unsafe_allow_html=True)
    fm = first_boker(chat, name)
    fm = str(int(fm * 100)) + '%'
    st.markdown(f"""כותב/ת <i>בוקר טוב</i> `{fm}` מהפעמים""", unsafe_allow_html=True)
    fm = first_night(chat, name)
    fm = str(int(fm * 100)) + '%'
    st.markdown(f"""כותב/ת <i>לילה טוב</i> `{fm}` מהפעמים""", unsafe_allow_html=True)


@st.cache
def get_responses_hist(chat, names):
    responses = chat['name'] != chat['name'].shift(1)
    responses.iloc[0] = False
    idx = np.where(responses)[0]

    diffs = pd.DataFrame([{
        'diff': (chat['datetime'].iloc[i] - chat['datetime'].iloc[i - 1]).seconds / 60,
        'name': chat['name'].iloc[i]
    } for i in idx], index=idx)
    print(len(diffs['name'].value_counts()))
    diffs = diffs[diffs['diff'] < np.quantile(diffs['diff'], 0.8)]
    hist_data = [diffs[diffs['name'] == name]['diff'] for name in names]
    # hist_data = [series[series < ] for series in hist_dsata]
    group_labels = names
    return hist_data, group_labels

def _display_massage_time_hist(chat, names):
    import plotly.figure_factory as ff
    hist_data, group_labels = get_responses_hist(chat, names)
    fig = ff.create_distplot(hist_data, group_labels)
    fig.update_layout(paper_bgcolor="#f1f1f1")
    fig.update_layout(plot_bgcolor="#f1f1f1")
    st.plotly_chart(fig, use_container_width=True)


@st.cache
def _get_mesanens(chat, names):
    from datetime import timedelta
    diff_time = chat['datetime'].diff() < timedelta(minutes=60)
    conv_idx = np.where(~diff_time)[0]
    conversations = [(conv_idx[i], conv_idx[i+1]) for i in range(len(conv_idx) - 1)]
    sihut_count = {name: 0 for name in names}
    mesanen_count = {name: 0 for name in names}

    print(1)

    def get_first_of_conv(conv):
        return conv.iloc[0]['name']
    def is_mesanen(conv):
        return conv['name'].nunique() == 1

    for c_s, c_e in conversations:
        conv = chat.iloc[c_s: c_e]
        if is_mesanen(chat.iloc[c_s: c_e]):
            mesanen_count[get_first_of_conv(conv)] += 1
        sihut_count[get_first_of_conv(conv)] += 1

    mesanen_precent = {names[idx]: np.round(mesanen_count[names[idx]] / sihut_count[names[2 + int(~bool(idx))]], 2) for idx in range(len(names))}
    return mesanen_count, sihut_count, mesanen_precent


def _display_sinunim(chat, name):
    names = chat['name'].unique()
    mesanen_count, sihut_count, mesanen_precent = _get_mesanens(chat, names)
    fm = mesanen_count[name]
    st.markdown(f"""סינן/ת `{fm}` פעמים""", unsafe_allow_html=True)
    fm = sihut_count[name]
    st.markdown(f"""התחיל/ה שיחה `{fm}` פעמים""", unsafe_allow_html=True)
    fm = str(int(mesanen_precent[name] * 100)) + '%'
    st.markdown(f"""סינן/ת `{fm}` מהפעמים""", unsafe_allow_html=True)

def app():
    st.title('סטטיסטיקות')

    st.write('קבלו סטטיסטיקות על השיחות')

    if not is_chat_exist():
        st.write('!העלה קובץ בדף הראשי')
        return

    chat = read_chat()
    names = chat['name'].unique()
    txt_dict = {name: get_text_for_name(chat, name) for name in names}
    do_for_all_names(names, lambda name: _title_name(name))

    st.title(""":זמנים וסינונים""")
    do_for_all_names(names, lambda name: _display_first_massage(chat, name))
    do_for_all_names(names, lambda name: _display_sinunim(chat, name))
    st.markdown(':היסטוגרמת זמני תגובות')
    _display_massage_time_hist(chat, names)

    st.title(""":אורכי הודעות""")
    # do_for_all_names(names, lambda name: _display_massage_len_hist(txt_dict[name]), title = "היסטוגרמת מילים")
    _display_massage_len_hist(txt_dict, names)

    do_for_all_names(names, lambda name: _display_max_massage_len(txt_dict[name]))

    st.title(""":מס' הודעות ממוצע""")
    do_for_all_names(names, lambda name: _display_average_massage(txt_dict[name], '❤'))
    do_for_all_names(names, lambda name: _display_average_massage(txt_dict[name], 'אוהב'))
    do_for_all_names(names, lambda name: _display_average_massage(txt_dict[name], 'אוהב אותך'))
    do_for_all_names(names, lambda name: _display_average_massage(txt_dict[name], 'מתגעגע'))
    st.title(""":אמוג'ים""")
    do_for_all_names(names, lambda name: _display_average_emoji(txt_dict[name]))

    st.title(':ענני מילים')
    do_for_all_names(names, lambda name: _display_wordcloud_name(txt_dict[name]), title="מילים נפוצות")
    do_for_all_names(names, lambda name: _display_emojicloud_name(txt_dict[name]), title="אמוג'ים נפוצים")
