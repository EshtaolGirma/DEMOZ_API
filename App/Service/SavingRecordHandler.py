from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from App.Model.models import saving_plan, saving_deposit
from App.Model.Databasemodel import SavingPlanRecord, SavingTransaction
from App import db

# Saving Plan Services


def GetListOfSavingPlan(user):
    result = SavingPlanRecord.query.filter_by(user_id=user).all()

    li = []
    for plan in result:
        x = {'title': plan.title,
             'Goal': plan.goal,
             'Saved': plan.saved_amount,
             'id': plan.id
             }
        li.append(x)
    list_of_plans = {'Saving Plans': li}
    return list_of_plans


def CreateSavingPlan(request, user):
    try:
        new_saving_plan = SavingPlanRecord()
        new_saving_plan.user_id = user
        new_saving_plan.title = request.json['title']
        new_saving_plan.description = request.json['description']
        new_saving_plan.goal = request.json['saving_goal']
        new_saving_plan.saved_amount = request.json['initial_amount']
        new_saving_plan.frequency = request.json['frequency']
        new_saving_plan.one_time_deposit = request.json['one_time_deposit']
        new_saving_plan.starting_date = datetime.strptime(
            request.json['starting_date'], '%Y-%m-%d')
        new_saving_plan.ending_date = datetime.strptime(
            request.json['ending_date'], '%Y-%m-%d')

        db.session.add(new_saving_plan)
        db.session.commit()

    except Exception as e:
        return 'Operation Create New Saving Plan Failed', 501

    return 201


def GetSavingPlanDetail(user, saving_id):
    try:
        plan = SavingPlanRecord.query.filter_by(
            user_id=user, id=saving_id).first()

        deposits = SavingTransaction.query.filter_by(
            saving_plan_id=plan.id).all()

    except Exception as e:
        return 'Plan not found', 404

    list_of_deposits = []
    for deposit in deposits:
        transaction = {
            'Deposited Amount': deposit.deposited_amount,
            'Deposit Date': {
                'Day': deposit.transaction_date.day,
                'Month': deposit.transaction_date.month,
                'Year': deposit.transaction_date.year,
            },
            'id': deposit.id
        }
        list_of_deposits.append(transaction)

    result = {'Plan': {
        'Title': plan.title,
        'Description': plan.description,
        'Goal': plan.goal,
        'Saved Amount': plan.saved_amount,
        'Frequency of Deposit': plan.frequency,
        'Amount to Deposit': plan.one_time_deposit,
        'Saving Started On': {
            'Day': plan.starting_date.day,
            'Month': plan.starting_date.month,
            'Year': plan.starting_date.year
        },
        'Saving Ending On': {
            'Day': plan.ending_date.day,
            'Month': plan.ending_date.month,
            'Year': plan.ending_date.year
        },
    },
        'Deposits': list_of_deposits
    }

    return result


def DeleteSavingPlan(user, saving_id):
    # saving plan deleting policy
    try:
        SavingPlanRecord.query.filter_by(
            user_id=user, id=saving_id).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete User Account Failed'

    return 'Account Deleted Successfully'


def UpdateSavingPlanDetail(user, saving_id, request):
    try:
        current_info = SavingPlanRecord.query.filter_by(
            user_id=user, id=saving_id).first()

        if request.json['title'] != '' and current_info.title != request.json['title']:
            current_info.title = request.json['title']

        if request.json['description'] != '' and current_info.description != request.json['description']:
            current_info.description = request.json['description']

        if request.json['saving_goal'] != 0 and current_info.goal != request.json['saving_goal']:
            current_info.goal = request.json['saving_goal']

        if request.json['initial_amount'] != 0 and current_info.saved_amount != request.json['initial_amount']:
            current_info.saved_amount = request.json['initial_amount']

        if request.json['one_time_deposit'] != 0 and current_info.one_time_deposit != request.json['one_time_deposit']:
            current_info.one_time_deposit = request.json['one_time_deposit']

        if request.json['frequency'] != '' and current_info.frequency != request.json['frequency']:
            current_info.frequency = request.json['frequency']

        if request.json['starting_date'] != "":
            newdate = datetime.datetime.strptime(
                request.json['starting_date'], '%Y-%m-%d')
            if current_info.starting_date != newdate:
                current_info.starting_date = newdate

        if request.json['ending_date'] != "":
            newdate = datetime.datetime.strptime(
                request.json['ending_date'], '%Y-%m-%d')
            if current_info.ending_date != newdate:
                current_info.ending_date = newdate

        db.session.commit()

    except Exception as e:
        return 'Operation Update Saving Plan Details Failed'

    return GetSavingPlanDetail(user, saving_id)


# Saving Deposit Services


def CreateSavingDeposit(user, saving_id, request):
    try:
        new_deposit = SavingTransaction()
        new_deposit.saving_plan_id = saving_id
        new_deposit.deposited_amount = request.json['deposited_amount']
        new_deposit.transaction_date = datetime.strptime(
            request.json['deposit_day'], '%Y-%m-%d')
        new_deposit.description = request.json['description']

        saving = SavingPlanRecord.query.filter_by(id=saving_id).first()
        saving.saved_amount = saving.saved_amount + new_deposit.deposited_amount

        db.session.add(new_deposit)
        db.session.commit()
    except Exception as e:
        # return 'Operation Create a Saving Deposit Failed'
        return e

    return GetSavingPlanDetail(user, saving_id)


def GetSavingDepositDetail(user, saving_transaction):
    try:
        transaction = SavingTransaction.query.filter_by(
            id=saving_transaction).first()

    except Exception as e:
        return 'Transaction not found', 404

    result = {'Transaction': {
        'deposited_amount': transaction.deposited_amount,
        'Description': transaction.description,
        'Deposited On': {
            'Day': transaction.transaction_date.day,
            'Month': transaction.transaction_date.month,
            'Year': transaction.transaction_date.year
        },

    },
    }
    return result


def DeleteSavingDeposit(user, saving_transaction):
    try:
        SavingTransaction.query.filter_by(id=saving_transaction).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete User Account Failed', 501

    return 'Transaction Deleted Successfully', 200


def UpdateSavingDepositDetail(user, saving_transaction, request):
    try:
        current_info = SavingTransaction.query.filter_by(
            id=saving_transaction).first()

        if request.json['deposited_amount'] != '' and current_info.deposited_amount != request.json['deposited_amount']:
            current_info.deposited_amount = request.json['deposited_amount']

        if request.json['description'] != '' and current_info.descriptions != request.json['description']:
            current_info.descriptions = request.json['description']

        if request.json['deposit_day'] != "":
            newdate = datetime.datetime.strptime(
                request.json['deposit_day'], '%Y-%m-%d')
            if current_info.transaction_date != newdate:
                current_info.transaction_date = newdate

        db.session.commit()

    except Exception as e:
        return 'Operation Update Saving Transaction Details Failed', 501

    return GetSavingDepositDetail(user, saving_transaction)
