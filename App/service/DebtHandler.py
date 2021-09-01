from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from App.Model.Databasemodel import DebtsAndLoansRecord, DebtAndLoanTranaction, ContactPerson, IncomeRecord
from App.Service.ContactLibraryHandler import addNewContactPerson
from App import db


def GetListOfDebts(user):
    debts = DebtsAndLoansRecord.query.filter_by(
        user_id=user, debt_or_loan='d').all()

    li = []
    for debt in debts:
        contact = ContactPerson.query.filter_by(
            id=debt.involved_person).first()
        x = {'Title': debt.deal_title,
             'Amount': debt.initial_amount,
             'Loaner': contact.name,
             'id': debt.id
             }
        li.append(x)
    list_of_plans = {'List of Debts': li}
    return list_of_plans, 200


def CreateDebtRecord(user, request):  # created when a user take a loan from others
    try:
        # return id if the person exist : create new person
        loaner = addNewContactPerson(request.json['loaner_person'], user)
        new_debt_taken = DebtsAndLoansRecord()
        new_debt_taken.user_id = user
        new_debt_taken.deal_title = request.json['title']
        new_debt_taken.description = request.json['description']
        new_debt_taken.initial_amount = request.json['amount_of_debt_taken']
        new_debt_taken.debt_or_loan = 'd'  # default value
        new_debt_taken.involved_person = loaner
        new_debt_taken.deal_date = datetime.strptime(
            request.json['deal_done_on'], '%Y-%m-%d')

        income = IncomeRecord()
        income.user_id = user
        income.income_amount = new_debt_taken.initial_amount
        income.category = 'Loan'
        income.income_date = new_debt_taken.deal_date
        income.description = "Loan: " + new_debt_taken.deal_title

        db.session.add(new_debt_taken, income)
        db.session.commit()

    except Exception as e:
        return 'Operation Create Debt Failed', 501

    return 201


def GetDebtDetail(user, debt):
    try:
        debt = DebtsAndLoansRecord.query.filter_by(
            user_id=user, id=debt).first()

        repayments = DebtAndLoanTranaction.query.filter_by(
            deal_plan_id=debt.id).all()
        contact = ContactPerson.query.filter_by(
            id=debt.involved_person).first()

    except Exception as e:
        return 'Plan not found', 404

    list_of_repayment = []
    for repayment in repayments:
        transaction = {
            'Repaid Amount': repayment.returned_amount,
            'Repayment Date': {
                'Day': repayment.transaction_date.day,
                'Month': repayment.transaction_date.month,
                'Year': repayment.transaction_date.year,
            },
            'id': repayment.id
        }
        list_of_repayment.append(transaction)

    result = {'Debt Detail': {
        'Title': debt.deal_title,
        'Description': debt.description,
        'Brrowed amount': debt.initial_amount,
        'Repaid Amount': debt.paid_amount,
        'Loaner': contact.name,
        'Unpaid Amount': debt.initial_amount - debt.paid_amount,
        'Debt taken On': {
            'Day': debt.deal_date.day,
            'Month': debt.deal_date.month,
            'Year': debt.deal_date.year
        },
    },
        'Debt repayment list': list_of_repayment
    }

    return result, 200


def DeleteDebt(user, debt):
    try:
        DebtsAndLoansRecord.query.filter_by(
            user_id=user, id=debt).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete Debt Failed', 501

    return 'Debt Deleted Successfully', 201


def UpdateDebtDetail(user, debt, request):
    try:
        current_info = DebtsAndLoansRecord.query.filter_by(
            user_id=user, id=debt).first()

        if request.json['title'] != '' and current_info.deal_title != request.json['title']:
            current_info.deal_title = request.json['title']

        if request.json['description'] != '' and current_info.descriptions != request.json['description']:
            current_info.descriptions = request.json['description']

        if request.json['amount_of_debt_taken'] != 0 and current_info.initial_amount != request.json['amount_of_debt_taken']:
            current_info.initial_amount = request.json['amount_of_debt_taken']

        if request.json['loaner_person'] != '' and current_info.frequency != request.json['loaner_person']:
            loaner = addNewContactPerson(request['loaner_person'], user)
            current_info.frequency = loaner

        if request.json['deal_done_on'] != "":
            newdate = datetime.datetime.strptime(
                request.json['deal_done_on'], '%Y-%m-%d')
            if current_info.deal_date != newdate:
                current_info.deal_date = newdate
        db.session.commit()

    except Exception as e:
        return 'Operation Update Debt Details Failed', 501

    return GetDebtDetail(user, debt)


# Debt repayment Services


def CreateDebtRepayment(user, debt, request):
    try:
        debt_record = DebtsAndLoansRecord.query.filter_by(id=debt).first()

        new_repayment = DebtAndLoanTranaction()
        new_repayment.deal_plan_id = debt
        try:
            unpaid_amount = debt_record.initial_amount - debt_record.paid_amount
            new_payment = request.json['returned_amount']
            if unpaid_amount == 0:
                raise NotImplementedError()
            if new_payment <= unpaid_amount:
                new_repayment.returned_amount = new_payment
                debt_record.paid_amount = debt_record.paid_amount + new_repayment.returned_amount
            else:
                raise Exception()
        except NotImplementedError:
            return "Debt Paid Fully!"
        except Exception:
            return "Exceeded debt amount! Payment should be less than " + str(unpaid_amount)
        new_repayment.transaction_date = datetime.strptime(
            request.json['transaction_date'], '%Y-%m-%d')
        new_repayment.description = request.json['description']

        db.session.add(new_repayment)
        db.session.commit()
    except Exception as e:
        return 'Operation Create a debt return Failed', 501

    return GetDebtDetail(user, debt)


def GetDebtRepaymetDetail(user, debt_repayment):
    try:
        repayment = DebtAndLoanTranaction.query.filter_by(
            id=debt_repayment).first()

        debt = DebtsAndLoansRecord.query.filter_by(
            id=repayment.deal_plan_id).first()

    except Exception as e:
        return 'Data not found', 404

    result = {'Repayment': {
        'Debt Title': debt.deal_title,
        'Returned amount': repayment.returned_amount,
        'Description': repayment.description,
        'Repaid On': {
            'Day': repayment.transaction_date.day,
            'Month': repayment.transaction_date.month,
            'Year': repayment.transaction_date.year
        },

    },
    }

    return result, 200


def DeleteDebtRepayment(user, debt_repayment):
    try:
        DebtAndLoanTranaction.query.filter_by(id=debt_repayment).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete Debt repayment record Failed', 501

    return 'Record Deleted Successfully', 200


def UpdateDebtRepaymentDetail(user, debt_repayment, request):
    try:
        current_info = DebtAndLoanTranaction.query.filter_by(
            id=debt_repayment).first()

        debt_record = DebtsAndLoansRecord.query.filter_by(
            id=current_info.deal_plan_id).first()

        if request.json['returned_amount'] != 0 and current_info.returned_amount != request.json['returned_amount']:
            try:
                debt_record.paid_amount = debt_record.paid_amount - \
                    current_info.returned_amount
                unpaid_amount = debt_record.initial_amount - debt_record.paid_amount
                new_payment = request.json['returned_amount']
                if new_payment <= unpaid_amount:
                    current_info.returned_amount = new_payment
                    debt_record.paid_amount = debt_record.paid_amount + new_payment
                else:
                    raise NotImplementedError()
            except NotImplementedError as e:
                return "Exceeded debt amount payment should be less than " + str(unpaid_amount)

        if request.json['description'] != '' and current_info.description != request.json['description']:
            current_info.description = request.json['description']

        if request.json['transaction_date'] != "":
            newdate = datetime.datetime.strptime(
                request.json['transaction_date'], '%Y-%m-%d')
            if current_info.transaction_date != newdate:
                current_info.transaction_date = newdate

        db.session.commit()

    except Exception as e:
        return 'Operation Update Repayment Details Failed', 501

    return GetDebtRepaymetDetail(user, debt_repayment)
