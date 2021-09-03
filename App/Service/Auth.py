from flask import Flask, request
from flask_restplus import Api, Resource, Namespace
from flask_login import logout_user, login_user, login_required
from App import api
from App.Model.Databasemodel import UserRecord


auth = Namespace(
    'auth', description='Authentication and authorization control ')


@auth.route('/login/<user_email>/<user_password>/')
class Login(Resource):
    def post(self, user_email, user_password):
        """
        login user
        """
        try:

            user = UserRecord.query.filter_by(email=user_email).first()

            if user.password == user.password:
                login_user(user)

                return "Welcome"

        except Exception as e:
            return "Invalid login detail"


@auth.route('/logout/')
class Logout(Resource):

    @login_required
    def post(self):
        logout_user()
        return "user logged out"
