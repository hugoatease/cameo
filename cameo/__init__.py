from flask import Flask
import mongoengine
from redis import Redis
from gevent.pool import Pool

app = Flask(__name__)
app.config.from_object('settings')

mongoengine.connect(app.config['MONGODB_NAME'], host=app.config['MONGODB_HOST'], port=app.config['MONGODB_PORT'])
redis = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])

from api import api
api.init_app(app)

async_pool = Pool(size=1)