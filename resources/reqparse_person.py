from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('inn', required=True)
parser.add_argument('type', required=True)
parser.add_argument('shifer', required=True)
parser.add_argument('veriety', required=True)
parser.add_argument('status', required=True)
parser.add_argument('phone', required=True)
parser.add_argument('email', required=True)
