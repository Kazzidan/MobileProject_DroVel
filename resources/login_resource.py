import datetime

from flask import jsonify
from flask_restful import Resource, abort

from models import db_session
from models.token import RevokedTokenModel
from models.users import User
from resources.login_reqparse import parser
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                get_jwt_identity, get_jwt)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"Person {user_id} not found")


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if User.find_by_email(data['email']):
            return jsonify(
                message='User is already registered')
        else:
            new_user = User(
                email=data['email'],
                hashed_password=User.generate_hash(data['password'])
            )
            try:
                new_user.save_to_db()
                access_token = create_access_token(identity=data['email'])
                refresh_token = create_refresh_token(identity=data['email'])
                return jsonify(
                    message='User {} was created'.format(data['email']),
                    refresh_token=refresh_token,
                    access_token=access_token
                )
            except:
                return jsonify(
                    message='Something went wrong')


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_email(data['email'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}

        if User.verify_hash(data['password'], current_user.hashed_password):
            time_delta = datetime.timedelta(minutes=15)
            access_token = create_access_token(identity=data['email'],
                                               fresh=True, expires_delta=time_delta)  # , expires_delta=time_delta
            refresh_token = create_refresh_token(identity=data['email'])
            return jsonify(
                message='Logged in as {}'.format(current_user.email),
                refresh_token=refresh_token,
                access_token=access_token
            )
        else:
            return jsonify(
                message='Wrong credentials')


class UserLogoutAccess(Resource):
    @jwt_required(fresh=True)
    def post(self):
        jti = get_jwt()['jti']
        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            revoked_token = RevokedTokenModel(jti=jti, created_date=now)
            revoked_token.save_to_db()
            return jsonify(
                message='Access token has been revoked')
        except:
            return jsonify(
                message='Wrong credentials')


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    @jwt_required(fresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=True)
        return jsonify(access_token=access_token)


class OneUser(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({'person': users.to_dict(only=('name', 'about', 'email'))})


class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()


class SecretResource(Resource):
    @jwt_required(fresh=True)
    def get(self):
        return jsonify(
            answer=42
        )
