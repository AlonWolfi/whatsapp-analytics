import streamlit as st
import matplotlib.pyplot as plt
import emoji
from apps.extras.hebrew_stopwords import hebrew_stopwords, hebrew_alphabet
import re
from utils import is_chat_exist, read_chat
from wordcloud import WordCloud
import string
from config import DATA_DIR
import numpy as np

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
        return ''.join([c for c in text if c  in emojis ])
    text = chat[chat['name'] == name]['text']
    return text.apply(extract_emojis)

@st.cache
def generate_wordcloud(text_series):
    text = ' '.join(text_series.apply(reverse_text))
    emoji_unicodes = list(emoji.UNICODE_EMOJI['en'].keys())
    stopwords = hebrew_stopwords + hebrew_alphabet + emoji_unicodes + [t[1:-1] for t in TOKENS]
    stopwords = [reverse_text(word) for word in stopwords]
    wc = WordCloud(background_color="#f1f1f1", stopwords = stopwords, font_path=str(DATA_DIR / 'fonts'/'arial.ttf'), min_word_length=2).generate(text).recolor(colormap = 'tab10')
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

    wc = WordCloud(background_color="#f1f1f1",font_path=str(DATA_DIR / 'fonts'/'Symbola.ttf'), regexp=regexp).generate(text).recolor(colormap = 'tab10')
    return wc


def display_cloud(wc, with_streamlit = True):
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
    ae_len = average_massage(text, '[' + ''.join(list(emoji.UNICODE_EMOJI['en'].keys()))+ ']')
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
    series = series[series < np.quantile(series,0.996)]
    # hist = np.histogram(series, bins = 50, range = (0,np.quantile(series,0.998)))
    return series

def _display_massage_len_hist(txt_dict,names):
    import plotly.figure_factory as ff
    hist_data = [massage_len_hist(txt_dict[name]) for name in names]
    group_labels = names
    fig = ff.create_distplot(hist_data, group_labels)
    fig.update_layout(paper_bgcolor="#f1f1f1")
    fig.update_layout(plot_bgcolor="#f1f1f1")
    st.plotly_chart(fig, use_container_width=True)

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


    st.title(""":אורך הודעות""")
    # do_for_all_names(names, lambda name: _display_massage_len_hist(txt_dict[name]), title = "היסטוגרמת מילים")
    _display_massage_len_hist(txt_dict,names)   

    do_for_all_names(names, lambda name: _display_max_massage_len(txt_dict[name]))

    st.title(""":מס' הודעות ממוצע""")
    do_for_all_names(names, lambda name: _display_average_massage(txt_dict[name],'❤'))
    do_for_all_names(names, lambda name: _display_average_massage(txt_dict[name],'אוהב'))
    do_for_all_names(names, lambda name: _display_average_massage(txt_dict[name],'אוהב אותך'))
    do_for_all_names(names, lambda name: _display_average_massage(txt_dict[name],'מתגעגע'))
    st.title(""":אמוג'ים""")
    do_for_all_names(names, lambda name: _display_average_emoji(txt_dict[name]))



    st.title(':ענני מילים')
    do_for_all_names(names, lambda name: _display_wordcloud_name(txt_dict[name]), title = "מילים נפוצות")
    do_for_all_names(names, lambda name: _display_emojicloud_name(txt_dict[name]), title = "אמוג'ים נפוצים")

