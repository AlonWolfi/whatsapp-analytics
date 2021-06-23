import streamlit as st

def style_css():
    with open('extras/style.css') as f:
        style_css = f.read()
    st.markdown(f"""
        <style>
        {style_css}
        </style>
    """, unsafe_allow_html=True)
