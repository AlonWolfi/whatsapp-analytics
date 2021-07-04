"""Main app
"""
from apps import chat_generator, home, message_generator, statistics
from extras.header import header
from extras.multiapp import MultiApp
from extras.style import style_css


def init():
    from utils import init_tmp_dir
    init_tmp_dir()


def main(apps: list = []):
    init()

    style_css()
    header()
    # footer()
    main_app = MultiApp(apps=apps)
    main_app.run()


if __name__ == "__main__":
    main(apps=[
        {
            'title': 'בית',
            'app': home.app,
        },
        {
            'title': 'סטטיסטיקות',
            'app': statistics.app,
        },
        {
            'title': 'ייצר שיחה',
            'app': chat_generator.app,
        },
        {
            'title': 'השלם הודעה',
            'app': message_generator.app,
        },
    ])
