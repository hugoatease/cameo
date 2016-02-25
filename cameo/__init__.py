from flask import Flask, got_request_exception
import mongoengine
from redis import Redis
from gevent.pool import Pool
import rollbar
import os

app = Flask(__name__)
app.config.from_object('settings')

mongoengine.connect(app.config['MONGODB_NAME'], host=app.config['MONGODB_HOST'], port=app.config['MONGODB_PORT'])
redis = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])

async_pool = Pool(size=1)

if 'ROLLBAR_TOKEN' in app.config:
    rollbar.init(app.config['ROLLBAR_TOKEN'], 'flask',
                 root=os.path.dirname(os.path.realpath(__file__)), allow_logging_basic_config=False)

@app.before_first_request
def rollbar_handler():
    if 'ROLLBAR_TOKEN' in app.config:
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

from api import api
api.init_app(app)