from App import api
from App.Controller.DebtAndLoanRoute import debts, loans
from App.Controller.SavingRoute import saving
from App.Controller.RecurringPaymentRoute import bills
api.add_namespace(saving)
api.add_namespace(debts)
api.add_namespace(loans)
api.add_namespace(bills)
