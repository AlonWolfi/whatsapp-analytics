from apps import home, statistics, chat_generator
from extras.header import header
from extras.multiapp import MultiApp
from extras.style import style_css


def init():
    from utils import make_tmp_dir
    make_tmp_dir()


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
        }
    ])
