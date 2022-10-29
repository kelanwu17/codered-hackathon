from flask import Flask, render_template
import json
import requests
api_key = "lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3"
response = requests.get("https://api.eia.gov/v2/natural-gas/prod/oilwells/data/?api_key=lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3")

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import sqlite3
import os
import os.path
from functools import wraps
#def jprint(obj):
#    text = json.dumps(obj, sort_keys=True, indent= 4)
#    print(text)

#jprint(response.json())
#print(response.status_code)


app = Flask(__name__)

@app.route("/")
def home():
     return render_template("home.html")
"""
class SubmitForm(Form):
    startyear = StringField('StartYear')
    endyear = StringField('EndYear')
    selecttype = StringField('SelectType')
"""
@app.route('/submit',methods=['Get','POST'])
def submit():
    submit = {'start': '', 'end': '', 'selecttype': "",'state' : ""}
    if request.method == 'POST':  #if submit form
        start = request.form['start']
        end = request.form['end']
        selecttype = request.form['selecttype']
        states = request.form['state']

        return redirect(url_for('index'))
    return render_template('submit.html',submit = submit)


if __name__ == "__main__":
    app.run(debug=True)
