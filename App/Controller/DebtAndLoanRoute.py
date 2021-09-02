from App import api
from flask_login import login_required, current_user
from flask import Flask, request
from flask_restplus import Api, Resource, Namespace
from App.Model.models import debt_plan, debt_deposit, loan_plan, loan_collection
from App.Service.DebtHandler import GetListOfDebts, CreateDebtRecord, GetDebtDetail, DeleteDebt, UpdateDebtDetail, CreateDebtRepayment, GetDebtRepaymetDetail, DeleteDebtRepayment, UpdateDebtRepaymentDetail
from App.Service.LoanHandler import GetListOfLoans, CreateLoanRecord, GetLoanDetail, DeleteLoan, UpdateLoanDetail, CreateLoanCollection, GetLoanCollectionDetail, DeleteLoanCollection, UpdateLoanCollectionDetail

debts = Namespace('debts', description='Debt Plan Record Management')


@debts.route('/records/')
class DebtPlans(Resource):
    @login_required
    def get(self):
        """
        return json list of Debt Records
        """
        return GetListOfDebts(current_user.id)

    @api.expect(debt_plan)
    @login_required
    def post(self):
        """
        create a Debt Record
        """
        return CreateDebtRecord(current_user.id, request)


@debts.route('/<debts_plan_id>/')
class DebtPlan(Resource):
    @login_required
    def get(self, debts_plan_id):
        """
        return json of a Debt plan detail and deposit summary
        """
        return GetDebtDetail(current_user.id, debts_plan_id)

    @login_required
    def delete(self, debts_plan_id):
        """
        delete a Debt plan
        """
        return DeleteDebt(current_user.id, debts_plan_id)

    @api.expect(debt_plan)
    @login_required
    def put(self, debts_plan_id):
        """
        update a Debt plan detail
        """
        return UpdateDebtDetail(current_user.id, debts_plan_id, request)


@debts.route('/repayment/<debt_plan_id>/')
class NewDebtTransaction(Resource):
    @api.expect(debt_deposit)
    @login_required
    def post(self, debt_plan_id):
        """
        deposit to a Debt deposit
        """
        return CreateDebtRepayment(current_user.id, debt_plan_id, request)


@debts.route('/repayment/<debt_transaction_id>/')
class DebtTransaction(Resource):
    @login_required
    def get(self, debt_transaction_id):
        """
        return json of a Debt deposit detail
        """
        return GetDebtRepaymetDetail(current_user.id, debt_transaction_id)

    @login_required
    def delete(self, debt_transaction_id):
        """
        delete Debt deposit
        """
        return DeleteDebtRepayment(current_user.id, debt_transaction_id)

    @api.expect(debt_deposit)
    @login_required
    def put(self, debt_transaction_id):
        """
        edit Debt deposit details
        """
        return UpdateDebtRepaymentDetail(current_user.id, debt_transaction_id, request)


loans = Namespace('loans', description='Loan Record Management')


@loans.route('/records/')
class LoanRecords(Resource):
    @login_required
    def get(self):
        """
        return json list of Loans given out
        """
        return GetListOfLoans(current_user.id)

    @api.expect(loan_plan)
    @login_required
    def post(self):
        """
        create a Loan Record
        """
        return CreateLoanRecord(request, current_user.id)


@loans.route('/<loan_id>/')
class LoanRecord(Resource):
    @login_required
    def get(self, loan_id):
        """
        return json of a Loan detail and Collected payment summary
        """
        return GetLoanDetail(current_user.id, loan_id)

    @login_required
    def delete(self, loan_id):
        """
        delete a Loan Record
        """
        return DeleteLoan(current_user.id, loan_id)

    @api.expect(loan_plan)
    @login_required
    def put(self, loan_id):
        """
        update a Loan Record detail
        """
        return UpdateLoanDetail(current_user.id, loan_id, request)


@loans.route('/collection/<loan_id>/')
class NewLoanTransaction(Resource):
    @api.expect(loan_collection)
    @login_required
    def post(self, loan_id):
        """
        Collect loan payment
        """
        return CreateLoanCollection(current_user.id, loan_id, request)


@loans.route('/collection/<loan_collection_id>/')
class LoanTransaction(Resource):
    @login_required
    def get(self, loan_collection_id):
        """
        return json of a Loan payment detail
        """
        return GetLoanCollectionDetail(current_user.id, loan_collection_id)

    @login_required
    def delete(self, loan_collection_id):
        """
        delete Loan Payment record
        """
        return DeleteLoanCollection(current_user.id, loan_collection_id)

    @api.expect(loan_collection)
    @login_required
    def put(self, loan_collection_id):
        """
        edit Loan Payment record details
        """
        return UpdateLoanCollectionDetail(current_user.id, loan_collection_id, request)
