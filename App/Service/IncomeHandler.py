from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from App.Model.Databasemodel import IncomeRecord
from App import db


def GetListOfIncomes(user):
    income_list = IncomeRecord.query.filter_by(user_id=user).all()

    retsult = []
    for i in income_list:
        income_detail = {
            'Income Amount': i.income_amount,
            'Source': i.category,
            'Description': i.description,
            'Date': {
                'Day': i.income_date.day,
                'Month': i.income_date.month,
                'Year': i.income_date.year,
            },
        }
        retsult.append(income_detail)

    return {'List of Incomes': retsult}


def CreateIncome(user, request):
    try:
        new_income = IncomeRecord()
        new_income.user_id = user
        new_income.income_amount = request.json['income_amount']
        new_income.description = request.json['description']
        try:
            if request.json['category'] in ['Salary', 'Loan', 'Gift', 'Bonus', 'Deposit', 'Other']:
                new_income.category = request.json['category']
            else:
                raise Exception(
                    'Unknown Income Source! Income can be from Salary, Loan, Gift, Bonus, Deposit')
        except Exception as e:
            return e
        new_income.income_date = datetime.strptime(
            request.json['date'], '%Y-%m-%d')

        db.session.add(new_income)
        db.session.commit()

    except Exception as e:
        return 'Operation Create Income Failed', 501

    return 201


def UpdateIncome(user, income, request):
    try:
        current_info = IncomeRecord.query.filter_by(
            id=income).first()

        if request.json['income_amount'] != 0 and current_info.income_amount != request.json['description']:
            current_info.income_amount = request.json['income_amount']

        if request.json['category'] != '' and current_info.category != request.json['description']:
            try:
                if request.json['category'] in ['Salary', 'Loan', 'Gift', 'Bonus', 'Deposit', 'Other']:
                    current_info.category = request.json['category']
                else:
                    raise Exception(
                        'Unknown Income Source! Income can be from Salary, Loan, Gift, Bonus, Deposit')
            except Exception as e:
                return e

        if request.json['description'] != '' and current_info.description != request.json['description']:
            current_info.description = request.json['description']

        if request.json['date'] != "":
            newdate = datetime.datetime.strptime(
                request.json['date'], '%Y-%m-%d')
            if current_info.income_date != newdate:
                current_info.income_date = newdate

        db.session.commit()

    except Exception as e:
        return 'Operation Update Income Details Failed', 501

    return GetListOfIncomes(user)


def DeleteIncome(user, income):
    try:
        IncomeRecord.query.filter_by(
            user_id=user, id=income).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete Income Failed', 501

    return 'Debt Deleted Successfully', 201
