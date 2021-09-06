from flask import Flask, request
from flask_restplus import Api, Resource, Namespace
from flask_login import login_required, current_user
from App import api
from App.Model.models import income_model
from App.Service.IncomeHandler import GetListOfIncomes, CreateIncome, UpdateIncome, DeleteIncome


income = Namespace(
    'income', description='Income control ')


@income.route('/get/')
class GetIncomeRecord(Resource):
    @login_required
    def get(self):
        """
        get list of incomes
        """
        return GetListOfIncomes(current_user.id)


@income.route('/create/')
class CreateIncomeRecord(Resource):
    @api.expect(income_model)
    @login_required
    def post(self):
        """
        Add income
        """
        return CreateIncome(current_user.id, request)


@income.route('/update/<income_id>')
class UpdateIncomeRecord(Resource):
    @api.expect(income_model)
    @login_required
    def put(self, income_id):
        """
        edit income info
        """
        return UpdateIncome(current_user.id, income_id, request)


@income.route('/delete/<income_id>')
class DeleteIncomeRecord(Resource):
    @login_required
    def delete(self, income_id):
        """
        delete income
        """
        return DeleteIncome(current_user.id, income_id)
