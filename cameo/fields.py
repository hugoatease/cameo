from flask_restful import fields

instagram_fields = {
    'number': fields.String,
    'username': fields.String,
    'fullname': fields.String,
    'text': fields.String
}

media_fields = {
    'tag': fields.String,
    'date': fields.DateTime,
    'url': fields.String,
    'type': fields.String,
    'thumbnail_url': fields.String,
    'instagram': fields.Nested(instagram_fields)
}