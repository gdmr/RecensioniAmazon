import sqlite3
from flask import Flask, g
from CONTROLLER.controller import controller
from threading import Thread
#from utils.updaterev import update_reviews
import schedule
import time
from utils.crnn import CRNN
from utils.ocr import OCR

app = Flask(__name__)
app.secret_key = '100200300400500600'

app.register_blueprint(controller)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db', check_same_thread=False)
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        g._database = None

if __name__ == '__main__':
    #schedule.every(7).days.do(update_reviews)
    #schedule_thread = Thread(target=schedule.run_pending)
    #schedule_thread.start()
    app.run(debug=True, port=8000)

