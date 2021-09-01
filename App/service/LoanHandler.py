from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from App.Model.Databasemodel import DebtsAndLoansRecord, DebtAndLoanTranaction, ContactPerson
from App.Service.ContactLibraryHandler import addNewContactPerson
from App import db


def GetListOfLoans(user):
    loans = DebtsAndLoansRecord.query.filter_by(
        user_id=user, debt_or_loan='l').all()

    li = []
    for loan in loans:
        contact = ContactPerson.query.filter_by(
            id=loan.involved_person).first()
        x = {'Title': loan.deal_title,
             'Amount': loan.initial_amount,
             'Borrower': contact.name,
             'id': loan.id
             }
        li.append(x)
    list_of_plans = {'List of loans': li}
    return list_of_plans, 200


def CreateLoanRecord(request, user):  # created when a user gives loans
    try:
        # return id if the person exist : create new person
        loaner = addNewContactPerson(request.json['borrower'], user)
        new_loan_given = DebtsAndLoansRecord()
        new_loan_given.user_id = user
        new_loan_given.deal_title = request.json['title']
        new_loan_given.description = request.json['description']
        new_loan_given.initial_amount = request.json['amount_of_loan_given']
        new_loan_given.debt_or_loan = 'l'  # default value
        new_loan_given.involved_person = loaner
        new_loan_given.deal_date = datetime.strptime(
            request.json['deal_done_on'], '%Y-%m-%d')

        db.session.add(new_loan_given)
        db.session.commit()

    except Exception as e:
        return 'Operation Create Loan Failed', 501

    return 201


def GetLoanDetail(user, loan_id):
    try:
        loan = DebtsAndLoansRecord.query.filter_by(
            user_id=user, id=loan_id).first()

        collections = DebtAndLoanTranaction.query.filter_by(
            deal_plan_id=loan.id).all()
        contact = ContactPerson.query.filter_by(
            id=loan.involved_person).first()

    except Exception as e:
        return 'Record not found', 404

    list_of_collections = []
    for collection in collections:
        transaction = {
            'Collected Amount': collection.returned_amount,
            'collection Date': {
                'Day': collection.transaction_date.day,
                'Month': collection.transaction_date.month,
                'Year': collection.transaction_date.year,
            },
            'id': collection.id
        }
        list_of_collections.append(transaction)

    result = {'loan Detail': {
        'Title': loan.deal_title,
        'Description': loan.description,
        'Brrowed amount': loan.initial_amount,
        'Collected Amount': loan.paid_amount,
        'Borrower': contact.name,
        'Uncollected Amount': loan.initial_amount - loan.paid_amount,
        'Loan given On': {
            'Day': loan.deal_date.day,
            'Month': loan.deal_date.month,
            'Year': loan.deal_date.year
        },

    },
        'loan collection list': list_of_collections
    }

    return result, 200


def DeleteLoan(user, loan):
    try:
        DebtsAndLoansRecord.query.filter_by(
            user_id=user, id=loan).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete loan Failed', 501

    return 'loan Deleted Successfully', 201


def UpdateLoanDetail(user, loan, request):
    try:
        current_info = DebtsAndLoansRecord.query.filter_by(
            user_id=user, id=loan).first()

        if request.json['title'] != '' and current_info.deal_title != request.json['title']:
            current_info.deal_title = request.json['title']

        if request.json['description'] != '' and current_info.descriptions != request.json['description']:
            current_info.descriptions = request.json['description']

        if request.json['amount_of_loan_given'] != 0 and current_info.initial_amount != request.json['amount_of_loan_given']:
            current_info.initial_amount = request.json['amount_of_loan_given']

        if request.json['borrower'] != '' and current_info.frequency != request.json['borrower']:
            loaner = addNewContactPerson(request['borrower'], user)
            current_info.frequency = loaner

        if request.json['deal_done_on'] != "":
            newdate = datetime.datetime.strptime(
                request.json['deal_done_on'], '%Y-%m-%d')
            if current_info.deal_date != newdate:
                current_info.deal_date = newdate
        db.session.commit()

    except Exception as e:
        # return 'Operation Update Loan Details Failed', 501
        return e

    return GetLoanDetail(user, loan)
