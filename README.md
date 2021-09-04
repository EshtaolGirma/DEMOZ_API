# AMP Project: Demoz API
Our project is monthly expense managing app what we chose to name "Demoz" app.

//TO view the fullter app - https://github.com/EshtaolGirma/DEMOZ_Client_App
Our project is monthly expense managing app what we chose to name it "Demoz" app.

The app is aimed to be used for properly using a monthly income, by providing a mechanism to record and have quick acces to view all income and expenses. it also provide a better way to manage bills with a reminder to when the next payment date is, by calculating it based on the frequency of days inputted by the user. The app motivate to having a saving plan and following it through the plan by showing how many days and moeny left to reach the user goals. And When it comes to debt and loans it recordes who is the loaner and borrower and the amount of cash involved nad the date the deal was made.

# This is the Api side of the Demoz Application
The app includes the users monthly expense,  debt and lonad, saving record, income, and authentication and authorization (login and register) request handler endpoints. the api is built using flask rest-plus, sqlite and other packages listed in the requirements.txt file.


we have included 6 business features as listed below
1.User CRUD

2.authentication and authorization

3.notify due date for recurring transaction/payments

4.keep track of saving goal process

5.manage debt and loan payment process

6.record and summarize response

GROUP MEMBERS

1.BEKEN ADUGNA ETR/2532/11

2.ESHTAOL GIRMA ATR/7961/11

3.MIKIYAS DANIEL ATR/1876/11

4.REDIATE BEFEKADU ETR/0042/11

5.ZEKARIYAS ALEMU ATR/2880/11

# Get started

To install python virtual Environment

```python
pip install virtualenv
```

To activate Virtual Environment

```python
# for mac
source env/bin/activate
#for windows
\env\Scripts\activate.bat
```

To install python packages used

```python
pip install -r requirements.txt
```

To run the app

# Method 1

```python
python run.py
```

# Method 2

Set Flask_app variable equals to run.py

```python
export FLASK_APP=run.py
```

Run the app

```python
flask run
```
