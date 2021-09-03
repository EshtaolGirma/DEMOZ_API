from App import api
from flask_login import login_required, current_user
from flask import Flask, request
from flask_restplus import Api, Resource, Namespace
from App.Model.models import bills_plan, bills_deposit
from App.Service.RecurringPaymentHandler import GetListOfBillPlan, CreateBillPlan, GetBillPlanDetail, CreateBillDeposit, GetBillDepositDetail, DeleteBillDeposit, UpdateBillPlanDetail, UpdateBillDepositDetail, DeleteBillPlan

bills = Namespace('bills', description='Bill Payment Plan Record ')


@bills.route('/')
class BillPlans(Resource):
    @login_required
    def get(self):
        """
        return json list of Bill plan
        """
        return GetListOfBillPlan(current_user.id)

    @api.expect(bills_plan)
    @login_required
    def post(self):
        """
        create a Bill plan
        """
        return CreateBillPlan(request, current_user.id)


@bills.route('/<bills_plan_id>/')
class BillPlan(Resource):
    @login_required
    def get(self, bills_plan_id):
        """
        return json of a Bill plan detail and deposit summary
        """
        return GetBillPlanDetail(current_user.id, bills_plan_id)

    @login_required
    def delete(self, bills_plan_id):
        """
        delete a Bill plan
        """
        return DeleteBillPlan(current_user.id, bills_plan_id)

    @api.expect(bills_plan)
    @login_required
    def put(self, bills_plan_id):
        """
        update a Bill plan detail
        """
        return UpdateBillPlanDetail(current_user.id, bills_plan_id, request)


@bills.route('/payment/<bills_plan_id>/')
class NewBillTransaction(Resource):
    @api.expect(bills_deposit)
    @login_required
    def post(self, bills_plan_id):
        """
        deposit to a Bill deposit
        """
        return CreateBillDeposit(current_user.id, bills_plan_id, request)


@bills.route('/payment/<bill_transaction_id>/')
class BillTransaction(Resource):
    @login_required
    def get(self, bill_transaction_id):
        """
        return json of a Bill deposit detail
        """
        return GetBillDepositDetail(current_user.id, bill_transaction_id)

    @login_required
    def delete(self, bill_transaction_id):
        """
        delete Bill deposit
        """
        return DeleteBillDeposit(current_user.id, bill_transaction_id)

    @api.expect(bills_deposit)
    @login_required
    def put(self, bill_transaction_id):
        """
        edit Bill deposit details
        """
        return UpdateBillDepositDetail(current_user.id, bill_transaction_id, request)
