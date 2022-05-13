from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy

from models import db_session
from models.token import RevokedTokenModel
from resources import login_resource, person_resources, email_resources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'glushenko_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-glushenko'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flasksql'
conn_str = db_session.global_init("db/mars_explorer.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
db = SQLAlchemy(app)

migrate = Migrate(app, db_session)
api = Api(app, catch_all_404s=True)
jwt = JWTManager(app)

api.add_resource(login_resource.UserRegistration, '/registration')
api.add_resource(login_resource.UserLogin, '/login')
api.add_resource(login_resource.UserLogoutAccess, '/logout/access')
api.add_resource(login_resource.UserLogoutRefresh, '/logout/refresh')
api.add_resource(login_resource.TokenRefresh, '/token/refresh')
api.add_resource(login_resource.AllUsers, '/users')
api.add_resource(login_resource.OneUser, '/users/<int:user_id>')
api.add_resource(person_resources.PersonsListResource, '/persons')
api.add_resource(person_resources.PersonsResource, '/persons/<int:person_id>')
api.add_resource(email_resources.EmailsListResource, '/emails')
api.add_resource(login_resource.SecretResource, '/secret')


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = RevokedTokenModel.is_jti_blacklisted(jti)
    return token is not None


@app.route('/')
def hello_world():
    return jsonify(message='Hello, World!')


def main():
    app.run()


if __name__ == '__main__':
    main()
