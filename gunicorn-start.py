import platform
from application import app
from db.models import init_db
from utils.tracks import parse_tracks


HOST = '127.0.0.1'
PORT = 45678
DEBUG = False


def initialize():
    parse_tracks()
    init_db()


if platform.uname().system.lower()=='linux':
    print("Detected Linux, Preparing gunicorn")        
    import gunicorn.app.base
    class StandaloneApplication(gunicorn.app.base.BaseApplication):

        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

if __name__ == "__main__":
    if platform.uname().system.lower()=='linux':
        print("Detected Linux, Running Gunicorn")
        options = {
            'bind': '%s:%s' % (HOST, PORT),
            'workers': 2,
            # 'threads': number_of_workers(),
            'timeout': 120,
        }
        initialize()
        StandaloneApplication(app, options).run()
    else:
        print("Detected non Linux, Running in pure Flask")
        initialize()
        app.run(debug=DEBUG, host=HOST, port=PORT)