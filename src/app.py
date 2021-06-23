import streamlit as st
from extras.multiapp import MultiApp
from extras.style import style_css
from extras.footer import footer
from apps import home, data, model # import your app modules here

app = MultiApp()

st.markdown("""
# Multi-Page App

This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).

""")


style_css()
# Add all your application here
app.add_app("Home", home.app)
app.add_app("Data", data.app)
app.add_app("Model", model.app)
# The main app
app.run()
footer()
