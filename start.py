import sys
import schedule
import time

from app import app as application
from app import parse_tracks
from app import albums
from db.models import init_db

HOST = '127.0.0.1'
PORT = 45678
DEBUG = False

if __name__ == '__main__':
    yes_words = ['yes', 'y', 'true', '1', '--debug']

    if len(sys.argv) < 2:
        pass
    elif sys.argv[1].lower() in yes_words:
        DEBUG = True
    elif sys.argv[1] == '--debug' and sys.argv[2] in yes_words:
        DEBUG = True
    init_db()
    parse_tracks()
    application.run(host=HOST, port=PORT, debug=DEBUG)
