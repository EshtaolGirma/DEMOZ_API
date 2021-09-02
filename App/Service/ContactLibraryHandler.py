from App.Model.Databasemodel import ContactPerson, SpendingaccompliceRecord
from App import db


def addNewContactPerson(name, user):
    try:
        existing_person = ContactPerson.query.filter_by(
            name=name, user_id=user).first()
        return existing_person.id
    except Exception as e:

        new_person = ContactPerson()
        new_person.name = name
        new_person.user_id = user

        db.session.add(new_photo)
        db.session.commit()
        new_person = ContactPerson.query.order_by(
            ContactPerson.id.desc()).first()

        return new_person.id


def addExpenseAccomplice(user, name_list, expense):

    for name in name_list:

        accomplice_id = addNewContactPerson(name, user)

        new_accomplice = SpendingaccompliceRecord()

        new_accomplice.contact_id = accomplice_id
        new_accomplice.expense_id = expense

        db.session.add(new_accomplice)
        db.session.commit()

    new_acc = SpendingaccompliceRecord.query.order_by(
        SpendingaccompliceRecord.id.desc()).first()

    return new_acc.id
