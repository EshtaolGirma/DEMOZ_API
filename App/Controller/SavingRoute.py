from flask import Flask, request
from flask_restplus import Api, Resource, Namespace
from flask_login import login_required, current_user
from App import api
from App.Model.models import saving_plan, saving_deposit
from App.Model.Databasemodel import SavingPlanRecord
from App.Service.SavingRecordHandler import GetListOfSavingPlan, CreateSavingPlan, GetSavingPlanDetail, DeleteSavingPlan, UpdateSavingPlanDetail, CreateSavingDeposit, GetSavingDepositDetail, DeleteSavingDeposit, UpdateSavingDepositDetail

saving = Namespace('saving', description='Saving Plan Record ')


@saving.route('/plans/')
class SavingPlans(Resource):
    @login_required
    def get(self):
        """
        return json list of Saving plan
        """
        return GetListOfSavingPlan(current_user.id)

    @api.expect(saving_plan)
    @login_required
    def post(self):
        """
        create a saving plan
        """
        return CreateSavingPlan(request, current_user.id)


@saving.route('/plan/<saving_plan_id>/')
class SavingPlan(Resource):
    @login_required
    def get(self, saving_plan_id):
        """
        return json of a Saving plan detail and deposit summary
        """
        return GetSavingPlanDetail(current_user.id, saving_plan_id)

    @login_required
    def delete(self, saving_plan_id):
        """
        delete a saving plan
        """
        return DeleteSavingPlan(current_user.id, saving_plan_id)

    @api.expect(saving_plan)
    @login_required
    def put(self, saving_plan_id):
        """
        update a saving plan detail
        """
        return UpdateSavingPlanDetail(current_user.id, saving_plan_id, request)


@saving.route('/transaction/<saving_plan_id>/')
class NewSavingTransaction(Resource):
    @api.expect(saving_deposit)
    @login_required
    def post(self, saving_plan_id):
        """
        deposit to a saving deposit
        """
        return CreateSavingDeposit(current_user.id, saving_plan_id, request)


@saving.route('/transaction/<saving_transaction_id>/')
class SavingTransaction(Resource):
    @login_required
    def get(self, saving_transaction_id):
        """
        return json of a saving deposit detail
        """
        return GetSavingDepositDetail(current_user.id, saving_transaction_id)

    @login_required
    def delete(self, saving_transaction_id):
        """
        delete saving deposit
        """
        return DeleteSavingDeposit(current_user.id, saving_transaction_id)

    @api.expect(saving_deposit)
    @login_required
    def put(self, saving_transaction_id):
        """
        edit saving deposit details
        """
        return UpdateSavingDepositDetail(current_user.id, saving_transaction_id, request)
