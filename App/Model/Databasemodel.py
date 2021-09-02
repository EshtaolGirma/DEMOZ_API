from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import CheckConstraint
from flask_login import UserMixin
from App import db


class PhotoLibrary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_uri = db.Column(db.String(120), unique=True, nullable=False)


class UserRecord(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    income = db.Column(db.Float, default=0.0)
    expense = db.Column(db.Float, default=0.0)
    password = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.Integer, db.ForeignKey(PhotoLibrary.id))


class ContactPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        UserRecord.id), nullable=False)
    name = db.Column(db.String(100), nullable=False)


class SavingPlanRecord(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        UserRecord.id), nullable=False)
    goal = db.Column(db.Float, nullable=False)
    saved_amount = db.Column(db.Float, default=0.0)
    one_time_deposit = db.Column(db.Float, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String(300))
    frequency = db.Column(db.Integer, nullable=False)
    starting_date = db.Column(db.DateTime, nullable=False)

    ending_date = db.Column(db.DateTime, nullable=False)


class DebtsAndLoansRecord(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        UserRecord.id), nullable=False)
    deal_title = db.Column(db.String(50), nullable=False)
    deal_date = db.Column(db.DateTime, nullable=False)
    involved_person = db.Column(db.Integer, db.ForeignKey(
        ContactPerson.id), nullable=False)
    initial_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, default=0.0)
    debt_or_loan = db.Column(db.Integer, nullable=False)
    db.CheckConstraint(debt_or_loan in ('d', 'l'))
    description = db.Column(db.String(300))


class RecurringPaymentRecord(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        UserRecord.id), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    bill_title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300))
    frequency = db.Column(db.String(10), nullable=False)
    starting_date = db.Column(db.DateTime, nullable=False)
    next_payment_date = db.Column(db.DateTime)


# other transcation record table


class SavingTransaction(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    saving_plan_id = db.Column(db.Integer, db.ForeignKey(
        SavingPlanRecord.id), nullable=False)
    deposited_amount = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(300))


class DebtAndLoanTranaction(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    deal_plan_id = db.Column(db.Integer, db.ForeignKey(
        DebtsAndLoansRecord.id), nullable=False)
    returned_amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(300))


class RecurringPaymentTranaction(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    recurring_payment_plan_id = db.Column(db.Integer, db.ForeignKey(
        RecurringPaymentRecord.id), nullable=False)
    bill_amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(300))


# Day to day expense table


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(20), unique=True, nullable=False)


class BudgetRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        UserRecord.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        Categories.id), nullable=False)
    budget_amount = db.Column(db.Integer, nullable=True, default=0)


class ExpenseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        UserRecord.id), nullable=False)
    spent_amount = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        Categories.id), nullable=False)
    expense_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(300))


class SpendingaccompliceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(
        ContactPerson.id), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey(
        ExpenseRecord.id), nullable=False)

# income record table


class IncomeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        UserRecord.id), nullable=False)
    income_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    db.CheckConstraint(category in (
        'Salary', 'Loan', 'Gift', 'Bonus', 'Deposit', 'Other'))
    income_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(300))


def createDatabase():
    db.create_all()


def importCategories():
    ListOfCategories = ['Food and Drink', 'Transportation', 'Mobile Pre-paid', 'Fuel', 'Kids',
                        'Clothes', 'Entrainment', 'Gifts', 'Holidays', 'Health', 'Rentals', 'Sports', 'Shoping']
    for cat in ListOfCategories:
        new_cat = Categories(category_name=cat)
        db.session.add(new_cat)

    db.session.commit()
