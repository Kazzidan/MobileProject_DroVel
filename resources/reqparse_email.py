from flask_restful import reqparse

parser_email = reqparse.RequestParser()
parser_email.add_argument('email', required=True)

