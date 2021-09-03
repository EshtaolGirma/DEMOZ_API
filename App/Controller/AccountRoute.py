from flask import Flask, request
from flask_login import login_required, current_user
from flask_restplus import Api, Resource, Namespace
from App import api
from App.Model.models import user_model
from App.Service.AccountEndpointHandler import GetUserInfo, CreateNewUserAccount, DeleteUserAccount, UpdateUserAccount

account = Namespace('account', description='Account control ')


@account.route('/')
class Account(Resource):
    @login_required
    def get(self):
        """
        Display User Account Info
        """
        return GetUserInfo(current_user.id)

    @login_required
    def delete(self):
        """
        Delete User Account
        """
        return DeleteUserAccount(current_user.id)

    @login_required
    @api.expect(user_model)
    def put(self):
        """
        Update User Account Info
        """
        return UpdateUserAccount(request, current_user.id)


@account.route('/SignUp/')
class NewAccount(Resource):
    @api.expect(user_model)
    def post(self):
        """
        Create New User Account
        """
        return CreateNewUserAccount(request)
