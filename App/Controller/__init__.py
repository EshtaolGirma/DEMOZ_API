from App import api
from App.Controller.DebtAndLoanRoute import debts, loans
from App.Controller.SavingRoute import saving
from App.Controller.DailyTransactionRoute import transaction

api.add_namespace(transaction)
api.add_namespace(saving)
api.add_namespace(debts)
api.add_namespace(loans)
