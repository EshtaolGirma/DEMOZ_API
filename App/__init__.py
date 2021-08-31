from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Demoz_Database.sqlite'
app.config['SECRET_KEY'] = 'DemozApiSecretKey'

db = SQLAlchemy(app)



api = Api(app, version='1.0', title='Demoz API',
          description='Expense Management API')


# from App.Model.Databasemodel import createDatabase

# createDatabase()
