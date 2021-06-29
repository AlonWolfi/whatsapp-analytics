import streamlit as st
import pandas as pd
import datetime

def parse_time(line_substr):
    dt = datetime.datetime.strptime(line_substr, '%d.%m.%Y, %H:%M')
    return dt

def join_seq_lines(lines):
    added_lines = []
    for line in lines:
        try:
            parse_time(line.split(' - ')[0])
            added_lines.append(line)
        except:
            added_lines[-1] += line
    return added_lines

def parse_line(line,dt_char = ' - ', name_char = ': '):
    dt_split = line.split(dt_char)
    dt = parse_time(dt_split[0])
    line = dt_char.join(dt_split[1:])

    name_split = line.split(name_char)
    name = name_split[0]
    text = name_char.join(name_split[1:])
    # removes last \n
    text = text[:-1]
    return pd.Series({
        'datetime': dt,
        'name': name,
        'text': text
    })

@st.cache
def chat_parser(lines):

    lines = join_seq_lines(lines)
    chat = pd.Series(lines).apply(parse_line)
   
    return chat