from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from App.Model.Databasemodel import ExpenseRecord, SpendingaccompliceRecord, BudgetRecord, Categories, ContactPerson
from App.Service.ContactLibraryHandler import addExpenseAccomplice
from App import db

# needs further optimization


def GetExpensesByCategory(user):
    try:
        expenses = ExpenseRecord.query.filter_by(user_id=user).all()

        cats = Categories.query.all()
    except Exception as e:
        return 'Server not responding', 500

    expense_list = {}
    for cat in cats:
        expense_list[cat.category_name] = []

    for expense in expenses:
        expense_cat = Categories.query.filter_by(
            id=expense.category_id).first()
        other_person = SpendingaccompliceRecord.query.filter_by(
            expense_id=expense.id).all()
        people = []
        for person in other_person:
            info = ContactPerson.query.filter_by(id=person.contact_id).first()
            person_name = info.name
            people.append(person_name)
        x_expense = {
            'Amount': expense.spent_amount,
            'Description': expense.description,
            'Date': {
                'Day': expense.expense_date.day,
                'Month': expense.expense_date.month,
                'Year': expense.expense_date.year,
            },
            'With': {
                'Contacts': people
            },
            'id': expense.id
        }

        expense_list[expense_cat.category_name].append(x_expense)

    return expense_list


def GetExpensesByCategorySummery(user):
    summery_list = GetExpensesByCategory(user)

    cats = Categories.query.all()

    for cat in cats:
        budget = BudgetRecord.query.filter_by(category_id=cat.id).first()
        total = 0
        for i in summery_list[cat.category_name]:
            total += i['Amount']

        summery_list[cat.category_name] = {'Total': total, 'Budget': budget}

    return summery_list, 200


def GetExpensesByCategoryDetail(user, category):
    expense_list = GetExpensesByCategory(user)
    cat = Categories.query.filter_by(id=category).first()

    return {cat.category_name: expense_list[cat.category_name]}


def GetExpenseDetail(user, expense_id):
    try:
        expense = ExpenseRecord.query.filter_by(
            user_id=user, id=expense_id).first()

        other_person = SpendingaccompliceRecord.query.filter_by(
            expense_id=expense.id).all()
    except Exception as e:
        return "Server not responding", 500

    people = []
    for person in other_person:
        info = ContactPerson.query.filter_by(id=person.contact_id).first()

        people.append(info.name)

    expense_detail = {
        'Spent Amount': expense.spent_amount,
        'Category': expense.category_id,
        'Description': expense.description,
        'With': people,
        'Spend On': {
            'Day': expense.expense_date.day,
            'Month': expense.expense_date.month,
            'Year': expense.expense_date.year,
        },
    }

    return {'Expense Detail': expense_detail}


def CreateNewExpense(user, category, request):
    try:
        new_expense = ExpenseRecord()
        new_expense.user_id = user
        new_expense.spent_amount = request.json['spent_amount']
        new_expense.description = request.json['description']
        new_expense.category_id = category
        acc_name = request.json['spent_with'].split(',')
        new_expense.expense_date = datetime.strptime(
            request.json['expense_day'], '%Y-%m-%d')

        db.session.add(new_expense)
        db.session.commit()
        addExpenseAccomplice(user, acc_name, new_expense.id)

    except Exception as e:
        return 'Operation Create Expense Failed', 501

    return 201


def UpdateExpense(user, expense, request):
    try:
        current_info = ExpenseRecord.query.filter_by(
            id=expense).first()

        acc_info = SpendingaccompliceRecord.query.filter_by(
            id=expense).first()
        acc_name = ContactPerson.query.filter_by(
            id=acc_info.contact_id).first()

        if request.json['spent_amount'] != '' and current_info.spent_amount != request.json['spent_amount']:
            current_info.spent_amount = request.json['spent_amount']

        if request.json['description'] != '' and current_info.description != request.json['description']:
            current_info.description = request.json['description']

        if request.json['spent_with'] != '' and acc_name.name != request.json['spent_with']:
            addExpenseAccomplice(
                user, request.json['spent_with'].split(','), expense)

        if request.json['expense_day'] != "":
            newdate = datetime.datetime.strptime(
                request.json['expense_day'], '%Y-%m-%d')
            if current_info.expense_date != newdate:
                current_info.expense_date = newdate

        db.session.commit()

    except Exception as e:
        return 'Operation Update Expense Details Failed', 501

    return GetExpenseDetail(user, expense)


def DeleteExpense(user, expense):
    try:
        ExpenseRecord.query.filter_by(
            user_id=user, id=expense).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete Expense Failed', 501

    return 'Expense Deleted Successfully', 201
