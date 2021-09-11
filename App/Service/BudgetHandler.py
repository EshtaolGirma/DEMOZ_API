from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
# from App.Model.models import saving_plan, saving_deposit
from App.Model.Databasemodel import BudgetRecord, Categories
from App import db


def GetListOfBudget(user):
    all_categories = Categories.query.all()

    list_of_expense_limits = {}
    for category in all_categories:
        try:
            limit = BudgetRecord.query.filter_by(
                category_id=category.id, user_id=user)
            list_of_expense_limits[category.category_name] = limit.budget_amount
        except Exception as e:
            list_of_expense_limits[category.category_name] = 0

    return {'List of expense Limits': list_of_expense_limits}


def CreateBudget(user, category, budget):
    try:
        new_budget = BudgetRecord(category_id=category, budget_amount=budget)
    except Exception as e:
        return 'Operation create budget Failed', 501
    return 201


def UpdateIncome(user, b_id, budget):
    try:
        current_info = BudgetRecord.query.filter_by(
            id=b_id).first()

        current_info.budget_amount = budget

        db.session.commit()

    except Exception as e:
        return 'Operation Update Budget Details Failed', 501

    return 200


def DeleteBudget(user, budget):
    try:
        BudgetRecord.query.filter_by(
            user_id=user, id=budget).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete Budget Failed', 501

    return 'Budget Deleted Successfully', 201
