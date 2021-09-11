import re
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user
from App.Model.models import saving_plan, saving_deposit
from App.Model.Databasemodel import UserRecord, PhotoLibrary, ContactPerson
from App.Service.PhotoLibraryHandler import AddPhoto
from App import db


def GetUserInfo(user):
    try:
        userInfo = UserRecord.query.filter_by(id=user).first()
    except Exception as e:
        return 'User not found'

    result = {'user': [{
        'Full Name': userInfo.full_name,
        'Email': userInfo.email,
        'Income': userInfo.income,
        'Expense': userInfo.expense,
    }]}
    return result


def GetUserContact(user):
    try:
        contacts = ContactPerson.query.filter_by(user_id=user).all()
    except Exception as e:
        return e
    list_contact = []
    for i in contacts:
        list_contact.append(i.name)

    return {'Contacts': list_contact}


def CreateNewUserAccount(request):
    try:
        if (EmailValidator(request.json['Email']) == False):
            return 'Invalid email'

        if (request.json['First_Name'].isalpha() == False or request.json['Last_Name'].isalpha() == False):
            return 'Invalid Name! Names can only contain alphabets'

        if (PasswordValidator(request.json['Password']) != True):
            return PasswordValidator(request.json['Password'])

        # photo = AddPhoto(request)
        new_user = UserRecord()
        new_user.full_name = request.json['First_Name'] + \
            ' ' + request.json['Last_Name']
        new_user.email = request.json['Email']
        new_user.password = request.json['Password']
        # new_user.avatar = photo

        db.session.add(new_user)
        db.session.commit()

        userIn = UserRecord.query.order_by(UserRecord.id.desc()).first()

    except Exception as e:
        return e

    login_user(userIn)
    return GetUserInfo(userIn.id)


def UpdateUserAccount(request, user):
    # the best way to update info 1. to send all the data again 2. allow empty fields
    try:
        current_info = UserRecord.query.filter_by(id=user).first()
        if (request.json['Email'] != ''):
            if (EmailValidator(request.json['Email']) == False):
                return 'Invalid email'
            if current_info.email != request.json['Email']:
                current_info.email = request.json['Email']
        if (request.json['First_Name'] != '' and request.json['Last_Name'] != ''):
            if (request.json['First_Name'].isalpha() == False or request.json['Last_Name'].isalpha() == False):
                return 'Invalid Name! Names can only contain alphabets'
        if (request.json['Password'] != ''):
            if (PasswordValidator(request.json['Password']) != True):
                return PasswordValidator(request.json['Password'])
            if current_info.password != request.json['Password']:
                current_info.password = request.json['Password']

        if current_info.full_name != request.json['First_Name'] + \
                ' ' + request.json['Last_Name']:
            current_info.full_name = request.json['First_Name'] + \
                ' ' + request.json['Last_Name']

        db.session.commit()

    except Exception as e:
        # return 'Operation Update User Details Failed'
        return e

    return GetUserInfo(current_info.id)


def DeleteUserAccount(user):
    try:
        UserRecord.query.filter_by(id=user).delete()
        db.session.commit()
    except Exception as e:
        return 'Operation Delete User Account Failed'
    logout_user()
    return 'Account Deleted Successfully'


def PasswordValidator(password):
    if len(password) < 8:
        return "Make sure your password is at lest 8 letters"
    elif re.search('[0-9]', password) is None:
        return "Make sure your password has a number in it"
    elif re.search('[A-Z]', password) is None:
        return "Make sure your password has a capital letter in it"
    else:
        return True


def EmailValidator(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        return False
