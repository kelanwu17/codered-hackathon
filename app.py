from flask import Flask, render_template, Markup, request, redirect, url_for
import requests
import json
import pandas

#loading Oil Wells Data
api_key = "lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3"
response = requests.get("https://api.eia.gov/v2/natural-gas/prod/wells/data/?api_key=" + api_key + "&data[]=value")

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent= 4)
    print(text)
    

json_data = json.loads(response.text)
#inputing data into lists
texas_value = []
texas_period = []
for i in range(0, len(json_data["response"]["data"])):
    if json_data["response"]["data"][i]["area-name"] == "TEXAS":
        texas_value.append(json_data["response"]["data"][i]["value"])
        texas_period.append(json_data["response"]["data"][i]["period"])

#sorting the lists
sorted = False
while (sorted != True):
    sorted = True
    for i in range(0, len(texas_value) - 1):
        if texas_period[i] > texas_period[i+1]:
            temp_period = texas_period[i+1]
            texas_period[i+1] = texas_period[i]
            texas_period[i] = temp_period
            
            temp_value = texas_value[i+1]
            texas_value[i+1] = texas_value[i]
            texas_value[i] = temp_value
            sorted = False

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
@app.route('/submit',methods=['GET','POST'])
def submit():
    submit = {'start': '', 'end': '', 'selecttype': "",'state' : ""}
    if request.method == 'POST':  #if submit form
        start = request.form['start']
        end = request.form['end']
        selecttype = request.form['selecttype']
        states = request.form['state']
        #return redirect(url_for('line'))
        return redirect(url_for('line', start = start, end = end, selecttype = selecttype, states = states))
    return render_template('submit.html', submit = submit)

@app.route('/line<start> <end> <selecttype> <states>')
def line(start, end, selecttype, states):
    line_labels=texas_period
    line_values=texas_value
    return render_template('index.html', start = start, end = end, selecttype = selecttype, states = states, title='Number of Gas Producing Oil Wells in Texas', max=17000, labels=texas_period, values=texas_value)

if __name__ == "__main__":
    app.run(debug=True)
