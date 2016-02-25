import requests
from flask import current_app
from datetime import datetime
from pytz import utc
from schema import Media, Instagram
from cameo import redis


def has_already_media(url):
    if len(Media.objects(url=url)) > 0:
        return True
    return False


def instagram_add(tagname, last_id, max_tag_id=None):
    url = 'https://api.instagram.com/v1/tags/' + tagname + '/media/recent'
    params = {
        'client_id': current_app.config['INSTAGRAM_CLIENT_ID'],
        'count': '15',
    }

    if max_tag_id is not None:
        params['max_tag_id'] = max_tag_id

    response = requests.get(url, params=params).json()
    data = response['data']
    if 'next_max_tag_id' in response['pagination']:
        next_max_tag_id = response['pagination']['next_max_tag_id']
    else:
        next_max_tag_id = None

    if max_tag_id is None:
        redis.set('cameo.instagram.tag.' + tagname + '.last_id', data[0]['id'])

    complete = False
    for item in data:
        if item['id'] == last_id:
            complete = True
            break

        if item['type'] != 'image' and item['type'] != 'video':
            continue

        if item['type'] == 'image':
            type = 'photo'
            url = item['images']['standard_resolution']['url']
        else:
            type = 'video'
            url = item['videos']['standard_resolution']['url']

        if has_already_media(url):
            continue

        instagram= Instagram(
            number=item['id'],
            username=item['user']['username'],
            fullname=item['user']['full_name'],
            text=item['caption']['text']
        )

        media = Media(
            tag=tagname,
            url=url,
            type=type,
            date=utc.localize(datetime.utcfromtimestamp(float(item['created_time']))),
            instagram=instagram
        )

        if type == 'video':
            media.thumbnail_url = item['images']['standard_resolution']['url']
        media.save()

    if not complete and next_max_tag_id is not None:
        instagram_add(tagname, last_id, next_max_tag_id)


def instagram_realtime(batch):
    for item in batch:
        if item['object'] == 'tag':
            instagram_add(item['object_id'], redis.get('cameo.instagram.tag.' + item['object_id'] + '.last_id'))