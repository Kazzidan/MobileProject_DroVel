from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('personId', required=True)
parser.add_argument('phone', required=True)

