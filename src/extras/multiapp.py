import streamlit as st


class MultiApp:
    def __init__(self, apps:list = []):
        self.apps = apps
        self.counter = 10

    def add_app(self, app_dict):
        self.apps.append(app_dict)

    def sidebar(self):
        selected_app = self.apps[0]
        for app in self.apps:
            if st.sidebar.button(app['title']):
                selected_app = app
        return selected_app

    def run(self):
        selected_app = self.sidebar()
        selected_app['app']()
        
