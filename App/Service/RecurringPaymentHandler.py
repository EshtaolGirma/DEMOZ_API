import datetime
from flask_sqlalchemy import SQLAlchemy
from App.Model.models import saving_plan, saving_deposit
from App.Model.Databasemodel import RecurringPaymentRecord, RecurringPaymentTranaction
from App import db


def GetListOfBillPlan(user):
    bills = RecurringPaymentRecord.query.filter_by(user_id=user).all()

    li = []
    for bill in bills:
        x = {'title': bill.bill_title,
             'bill_amount': bill.payment_amount,
             'Deposit Date': {
                 'Day': bill.next_payment_date.day,
                 'Month': bill.next_payment_date.month,
                 'Year': bill.next_payment_date.year,
             },
             'id': bill.id
             }
        li.append(x)
    list_of_plans = {'Bills': li}
    return list_of_plans


def CreateBillPlan(request, user):
    try:
        new_bill = RecurringPaymentRecord()
        new_bill.user_id = user
        new_bill.bill_title = request.json['bill_title']
        new_bill.description = request.json['bill_description']
        new_bill.payment_amount = request.json['payment_amount']
        new_bill.frequency = request.json['frequency']
        new_bill.starting_date = datetime.datetime.strptime(
            request.json['starting_date'], '%Y-%m-%d')
        next_date = datetime.datetime.strptime(
            request.json['starting_date'], '%Y-%m-%d')
        new_bill.next_payment_date = next_date + \
            datetime.timedelta(days=int(request.json['frequency']))

        db.session.add(new_bill)
        db.session.commit()

    except Exception as e:
        return 'Operation Create New Bill Failed', 501

    return 201


def GetBillPlanDetail(user, bill_id):
    try:
        bill = RecurringPaymentRecord.query.filter_by(
            user_id=user, id=bill_id).first()

        deposits = RecurringPaymentTranaction.query.filter_by(
            recurring_payment_plan_id=bill.id).all()

    except Exception as e:
        return 'Bill not found', 404

    list_of_deposits = []
    for deposit in deposits:
        payment = {
            'paid Amount': deposit.bill_amount,
            'Deposit Date': {
                'Day': deposit.transaction_date.day,
                'Month': deposit.transaction_date.month,
                'Year': deposit.transaction_date.year,
            },
            'id': deposit.id
        }
        list_of_deposits.append(payment)

    result = {'Bill': {
        'Title': bill.bill_title,
        'Description': bill.description,

        'Payment Amount': bill.payment_amount,
        'Frequency': bill.frequency,
        'Bill Started On': {
            'Day': bill.starting_date.day,
            'Month': bill.starting_date.month,
            'Year': bill.starting_date.year
        },
        'Next Payment date On': {
            'Day': bill.next_payment_date.day,
            'Month': bill.next_payment_date.month,
            'Year': bill.next_payment_date.year
        },
    },
        'Payments': list_of_deposits
    }

    return result


def DeleteBillPlan(user, bill_id):
    try:
        RecurringPaymentRecord.query.filter_by(
            user_id=user, id=bill_id).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete Bill Failed'

    return 'Bill Deleted Successfully'


def UpdateBillPlanDetail(user, bill_id, request):
    try:
        current_info = RecurringPaymentRecord.query.filter_by(
            user_id=user, id=bill_id).first()

        if request.json['bill_title'] != '' and current_info.bill_title != request.json['bill_title']:
            current_info.bill_title = request.json['bill_title']

        if request.json['bill_description'] != '' and current_info.descriptions != request.json['bill_description']:
            current_info.descriptions = request.json['bill_description']

        if request.json['payment_amount'] != 0 and current_info.payment_amount != request.json['payment_amount']:
            current_info.payment_amount = request.json['payment_amount']

        if request.json['frequency'] != 0 and current_info.frequency != request.json['frequency']:
            current_info.frequency = request.json['frequency']

        if request.json['starting_date'] != "":
            newdate = datetime.datetime.strptime(
                request.json['starting_date'], '%Y-%m-%d')
            if current_info.starting_date != newdate:
                current_info.starting_date = newdate

        current_info.next_payment_date = current_info.starting_date + \
            datetime.timedelta(days=int(request.json['frequency']))

        db.session.commit()

    except Exception as e:
        # return 'Operation Update Bill Details Failed'
        return e

    return GetBillPlanDetail(user, bill_id)


# Bill Deposit Services


def CreateBillDeposit(user, bill_id, request):
    try:
        new_deposit = RecurringPaymentTranaction()
        new_deposit.recurring_payment_plan_id = bill_id
        new_deposit.bill_amount = request.json['bill_amount']
        new_deposit.transaction_date = datetime.datetime.strptime(
            request.json['transaction_date'], '%Y-%m-%d')
        new_deposit.description = request.json['description']

        bill = RecurringPaymentRecord.query.filter_by(
            user_id=user, id=bill_id).first()

        bill.next_payment_date = bill.next_payment_date + \
            datetime.timedelta(days=int(bill.frequency))

        db.session.add(new_deposit)
        db.session.commit()
    except Exception as e:
        # return 'Operation Create a Bill Transaction Failed'
        return e

    return GetBillPlanDetail(user, bill_id)


def GetBillDepositDetail(user, bill_transaction):
    try:
        transaction = RecurringPaymentTranaction.query.filter_by(
            id=bill_transaction).first()

        result = {'Transaction': {
            'deposited_amount': transaction.bill_amount,
            'Description': transaction.description,
            'Transaction Made On': {
                'Day': transaction.transaction_date.day,
                'Month': transaction.transaction_date.month,
                'Year': transaction.transaction_date.year
            },
        },
        }
    except Exception as e:
        return 'Transaction not found', 404

    return result


def DeleteBillDeposit(user, bill_transaction):
    try:
        RecurringPaymentTranaction.query.filter_by(
            id=bill_transaction).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete Bill payment Failed', 501

    return 'Transaction Deleted Successfully', 200


def UpdateBillDepositDetail(user, bill_payment, request):
    try:
        current_info = RecurringPaymentTranaction.query.filter_by(
            id=bill_payment).first()

        if request.json['bill_amount'] != "" and current_info.bill_amount != request.json['bill_amount']:
            current_info.bill_amount = request.json['bill_amount']

        if request.json['description'] != "" and current_info.description != request.json['description']:
            current_info.description = request.json['description']
        if request.json['transaction_date'] != "":
            newdate = datetime.datetime.strptime(
                request.json['transaction_date'], '%Y-%m-%d')
            if current_info.transaction_date != newdate:
                current_info.transaction_date = newdate

        db.session.commit()

    except Exception as e:
        return 'Operation Update Bill deposit Details Failed', 501

    return GetBillDepositDetail(user, bill_payment)
