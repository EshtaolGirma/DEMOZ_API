from App.Model.Databasemodel import ContactPerson
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
