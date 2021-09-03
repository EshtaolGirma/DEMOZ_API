from flask import Flask, request
from flask_restplus import Api, Resource, Namespace
from flask_login import login_required, current_user
from App.Model.models import expense_deposit
from App.Service.ExpenseHandler import CreateNewExpense, UpdateExpense, DeleteExpense, GetExpenseDetail, GetExpensesByCategoryDetail, GetExpensesByCategorySummery
from App import api

transaction = Namespace('transactions', description='Expense Record')


@transaction.route('/get/category/summery/')
class GetDailyTransactionByCategory(Resource):

    def get(self):
        """
        return json Expense
        """
        return GetExpensesByCategorySummery(current_user.id)


@transaction.route('/get/category/detail/<category_id>')
class GetDailyTransactionByCategoryDetail(Resource):

    def get(self, category_id):
        """
        return json Expense
        """
        return GetExpensesByCategoryDetail(current_user.id, category_id)


@transaction.route('/get/<expense_id>/')
class GetDailyTransactionDetail(Resource):

    def get(self, expense_id):
        """
        return json Expense
        """
        return GetExpenseDetail(current_user.id, expense_id, )


@transaction.route('/create/<category_id>/')
class CreateDailyTransaction(Resource):
    @api.expect(expense_deposit)
    def post(self, category_id):
        """
        create a Daily Transaction
        """
        return CreateNewExpense(current_user.id, category_id, request)


@transaction.route('/update/<expense_id>')
class UpdateDailyTransaction(Resource):
    @api.expect(expense_deposit)
    def put(self, expense_id):
        """
        update a Daily Transaction
        """
        return UpdateExpense(current_user.id, expense_id, request)


@transaction.route('/delete/<expense_id>/')
class DeleteDailyTransaction(Resource):
    def delete(self, expense_id):
        """
        Delete a Daily Transaction
        """
        return DeleteExpense(current_user.id, expense_id)
