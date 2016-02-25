from flask import request, current_app
import requests
from flask_restful import Api, Resource, abort, marshal_with
from uuid import uuid4
import hashlib, hmac
from instagram import instagram_realtime, instagram_add
from cameo import redis, async_pool
from schema import Media
from fields import media_fields

api = Api()


class InstagramSubscription(Resource):
    def post(self, tagname):
        params = {
            'client_id': current_app.config['INSTAGRAM_CLIENT_ID'],
            'client_secret': current_app.config['INSTAGRAM_CLIENT_SECRET'],
            'callback_url': current_app.config['INSTAGRAM_CALLBACK'],
            'aspect': 'media',
            'object': 'tag',
            'object_id': tagname
        }

        redis.set('cameo.instagram.tag.' + tagname + '.verify_token', uuid4())
        r = requests.post('https://api.instagram.com/v1/subscriptions/', data=params)
        redis.set('cameo.instagram.tag.' + tagname + '.subscription_id', r.json()['data']['id'])
        return r.content


class InstagramHub(Resource):
    @classmethod
    def check_signature(cls, signature, content):
        mac = hmac.new(current_app.config.INSTAGRAM_CLIENT_SECRET, digestmod=hashlib.sha1)
        mac.update(content)

        return signature == mac.hexdigest()

    def get(self):
        if 'hub.challenge' not in request.args:
            return abort(400)
        return request.args['hub.challenge']

    def post(self):
        if 'HTTP_X_HUB_SIGNATURE' not in request.headers:
            # Hub signature not provided
            return abort(401)

        if not self.check_signature(request.headers['HTTP_X_HUB_SIGNATURE'], request.data):
            # Invalid hub signature
            return abort(401)

        def instagram_event(data):
            with current_app.app_context():
                instagram_realtime(data)

        async_pool.apply_async(instagram_event, args=[request.get_json()])

        return 'OK'


class InstagramFetch(Resource):
    def post(self, tagname):
        instagram_add(tagname, redis.get('cameo.instagram.tag.' + tagname + '.last_id'))


class MediaApi(Resource):
    @marshal_with(media_fields)
    def get(self):
        return list(Media.objects())


api.add_resource(MediaApi, '/api/media')
api.add_resource(InstagramSubscription, '/api/instagram/subscriptions/<tagname>')
api.add_resource(InstagramHub, '/api/instagram/hub')
api.add_resource(InstagramFetch, '/api/instagram/<tagname>/fetch')