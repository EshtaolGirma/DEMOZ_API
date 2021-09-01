from App import api
from App.Controller.DebtAndLoanRoute import debts, loans


api.add_namespace(debts)
api.add_namespace(loans)
