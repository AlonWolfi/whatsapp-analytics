import streamlit as st
from htbuilder import img, styles


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def header():
    from config import DATA_DIR
    from PIL import Image

    imagee = Image.open(DATA_DIR / 'images' / 'whatsapp_cover.png').convert('RGB')
    st.image(imagee, use_column_width=True)
    # st.write("""
    # סמל וואטסאפ
    # """)


if __name__ == "__main__":
    header()