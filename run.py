import logging
from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format('log', 'output')),
        logging.StreamHandler()
    ])

app = Flask(__name__)


@app.route('/train')
def hello_world():
    return render_template('train.html')


@app.route('/chatroom_employee')
def chatroom_employee():
    return render_template('chatroom_employee.html')


@app.route('/chatroom_employer')
def chatroom_employer():
    return render_template('chatroom_employer.html')


app.wsgi_app = ProxyFix(app.wsgi_app)

from app.api import api
api.init_app(app)

app.run(host='0.0.0.0', debug=False)
