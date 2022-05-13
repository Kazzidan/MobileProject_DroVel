from flask_restful import reqparse

parser_ph = reqparse.RequestParser()
parser_ph.add_argument('phone', required=True)
