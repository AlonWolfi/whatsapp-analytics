import streamlit as st
from pathlib import Path

def write_style(style_file_name: str, css_folder = Path(__file__).resolve().parent / 'css'):
    with open(css_folder / style_file_name) as f:
        style_css = f.read()
    st.markdown(f"""
        <style>
        {style_css}
        </style>
    """, unsafe_allow_html=True)

def style_css():
    for style_path in ['style.css', 'backward_sidebar.css']:
        write_style(style_path)
