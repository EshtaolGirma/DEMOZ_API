from flask_restplus import fields
from App import api


user_model_templet = {
    'First_Name': fields.String,
    "Last_Name": fields.String,
    'Email': fields.String,
    'Password': fields.String,
    'Avatar': fields.String,
}


SavingPlan_model_templet = {
    'saving_goal': fields.Float,
    'initial_amount': fields.Float,
    'one_time_deposit': fields.Float,
    'title': fields.String,
    'description': fields.String,
    'frequency': fields.String,
    'starting_date': fields.Date,
    'ending_date': fields.Date

}


savingDeposit_model_templet = {
    'deposited_amount': fields.Float,
    'deposit_day': fields.Date,
    'description': fields.String,
}


DebtPlan_model_templet = {
    'title': fields.String,
    'description': fields.String,
    'amount_of_debt_taken': fields.Float,
    'deal_done_on': fields.Date,
    'loaner_person': fields.String,
}

DebtDeposit_model_templet = {
    'returned_amount': fields.Float,
    'transaction_date': fields.Date,
    'description': fields.String,
}

Loan_model_templet = {
    'title': fields.String,
    'description': fields.String,
    'amount_of_debt_taken': fields.Float,
    'deal_done_on': fields.Date,
    'borrower': fields.String,
}

Loan_Collection_model_templet = {
    'collected_amount': fields.Float,
    'transaction_date': fields.Date,
    'description': fields.String,
}
BillsPlan_model_templet = {
    'payment_amount': fields.Float,
    'bill_title': fields.String,
    'bill_description': fields.String,
    'frequency': fields.Integer,
    'starting_date': fields.Date,
}

BillsDeposit_model_templet = {
    'bill_amount': fields.Float,
    'transaction_date': fields.Date,
    'description': fields.String,
}


ExpenseDepsit_model_templeet = {
    'spent_amount': fields.Float,
    'expense_day': fields.Date,
    'spent_with': fields.String,
    'description': fields.String,

}

Income_model_templet = {
    'income_amount': fields.Float,
    'category': fields.String,
    'date': fields.Date,
    'description': fields.String,
}

user_model = api.model('User Account', user_model_templet)

saving_plan = api.model('Saving Plan', SavingPlan_model_templet)
saving_deposit = api.model('Saving Deposit', savingDeposit_model_templet)


debt_plan = api.model('Debt Plan', DebtPlan_model_templet)
debt_deposit = api.model('Debt Repayment', DebtDeposit_model_templet)


loan_plan = api.model('Loan Record', Loan_model_templet)
loan_collection = api.model('Loan Collection', Loan_Collection_model_templet)

bills_plan = api.model('Bills Plan', BillsPlan_model_templet)
bills_deposit = api.model('Bills Deposit', BillsDeposit_model_templet)

expense_deposit = api.model('Expense Deposit', ExpenseDepsit_model_templeet)

income_model = api.model('Income', Income_model_templet)
