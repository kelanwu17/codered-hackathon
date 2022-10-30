from flask import Flask,flash, render_template, Markup, request, redirect, url_for
import requests
import json
import pandas

#loading Oil Wells Data
# api_key = "lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3"
# response = requests.get("https://api.eia.gov/v2/natural-gas/prod/wells/data/?api_key=" + api_key + "&data[]=value")

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent= 4)
    print(text)
    

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
    else:
     return render_template('layout.html', submit = submit)
    
    """

@app.route('/submit',methods=['GET','POST'])
def submit():
    submit = {'start': '', 'end': '', 'selecttype': "",'state' : ""}
    result = []
    if request.method == 'POST':  #if submit form
        start = request.form['start']
        end = request.form['end']
        selecttype = request.form['selecttype']
        states = request.form['state']
        #return redirect(url_for('line'))
        #   
        if int(start) > int(end):
            flash("The input parameters is not a valid",'danger')
            return render_template('submit.html', submit = submit, start = "2001", end = "2003", selecttype = "gas pro", states = "TEXAS", title= "", max=100)
        result = convert(start, end, selecttype, states)
        return render_template('submit.html', submit = submit, start = result[0], end = result[1], selecttype = result[2], states = result[3], title= result[4], max=result[5], labels=result[6], values=result[7] ,avg_oil_prod = result[8], a_increase = result[9])
        #return redirect(url_for('line', start = start, end = end, selecttype = selecttype, states = states))
    start = "2001"
    end = "2003"
    selecttype = "gas pro"
    states = "TEXAS"
    result = convert(start,end,selecttype,states)
    return render_template('submit.html', submit = submit, start = result[0], end = result[1], selecttype = result[2], states = result[3], title= result[4], max=result[5])


def convert(start, end, selecttype, states):
    api_key = "lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3"
    
    #inputing data into lists
    texas_value = []
    texas_period = []
  
    response = requests.get("https://api.eia.gov/v2/natural-gas/prod/wells/data/?api_key=" + api_key + "&data[]=value")
    json_data = json.loads(response.text)
    title = ""
    
    if selecttype == "gas pro": # if select is gas production
        response = requests.get("https://api.eia.gov/v2/natural-gas/prod/wells/data/?api_key=" + api_key + "&data[]=value")
        json_data = json.loads(response.text)
        title = "Gas Production in " + states
    elif selecttype == "gas_withdr": #if select type is gas withrawal
        response = requests.get("https://api.eia.gov/v2/natural-gas/prod/sum/data/?api_key=" + api_key + "&data[]=value")
        json_data = json.loads(response.text)
        title = "Gas Withdrawal in " + states
    elif selecttype == "oil_res": #if select type is oil res
        response = requests.get("https://api.eia.gov/v2/natural-gas/prod/sum/data/?api_key=" + api_key + "&data[]=value")
        json_data = json.loads(response.text)
        title = "Oil Reserves in " + states
    elif selecttype == "oil_pro": #if select type is oil pro
        response = requests.get("https://api.eia.gov/v2/petroleum/crd/crpdn/data/?api_key=" + api_key + "&data[]=value")
        json_data = json.loads(response.text)
        title = "Oil Production in " + states
    

    for i in range(0, len(json_data["response"]["data"]) - 1):
        if int(json_data["response"]["data"][i]["period"]) >= float(int(start)) and int(json_data["response"]["data"][i]["period"]) <= float(int(end)) and json_data["response"]["data"][i]["area-name"] == states:
            texas_value.append(json_data["response"]["data"][i]["value"])
            texas_period.append(json_data["response"]["data"][i]["period"])
    #sort data
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
    max_value = max(texas_value)
    m = max_value//10
    sum = 0
    for i in range(len(texas_value)):
        sum += int(texas_value[i])
    avg_oil_prod = round(sum/len(texas_value),2)
    
    increase = []

    sum = 0
    for i in range(len(texas_value) - 1):
       increase.append((int(texas_value[i+1]) - int(texas_value[i]) ) / int(texas_value[i]) * 100)
    
    for i in range(len(increase)):
        sum = sum + increase[i]
    a_increase = round(sum/len(increase),2)
    
    lst = [start,end,selecttype,states,title,m,texas_period,texas_value,avg_oil_prod, a_increase]
    return lst

@app.route('/line/<start>/<end>/<selecttype>/<states>')
def line(start, end, selecttype, states):
    api_key = "lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3"
    
    #inputing data into lists
    texas_value = []
    texas_period = []
  
    response = requests.get("https://api.eia.gov/v2/natural-gas/prod/wells/data/?api_key=" + api_key + "&data[]=value")
    json_data = json.loads(response.text)
    title = ""
    if selecttype == "gas pro": # if select is gas production
        response = requests.get("https://api.eia.gov/v2/natural-gas/prod/wells/data/?api_key=" + api_key + "&data[]=value")
        json_data = json.loads(response.text)
        title = "Gas Production in " + states
    elif selecttype == "gas_withdr": #if select type is gas withrawal
        response = requests.get("https://api.eia.gov/v2/natural-gas/prod/sum/data/?api_key=" + api_key + "&data[]=value")
        json_data = json.loads(response.text)
        title = "Gas Withdrawal in " + states
    elif selecttype == "oil_res": #if select type is oil res
        response = requests.get("https://api.eia.gov/v2/natural-gas/prod/sum/data/?api_key=" + api_key + "&data[]=value")
        json_data = json.loads(response.text)
        title = "Oil Reserves in " + states
    elif selecttype == "oil_pro": #if select type is oil pro
        response = requests.get("https://api.eia.gov/v2/petroleum/crd/crpdn/data/?api_key=" + api_key + "&data[]=value")
        json_data = json.loads(response.text)
        title = "Oil Production in " + states
    

    for i in range(0, len(json_data["response"]["data"]) - 1):
        if int(json_data["response"]["data"][i]["period"]) >= float(int(start)) and int(json_data["response"]["data"][i]["period"]) <= float(int(end)) and json_data["response"]["data"][i]["area-name"] == states:
            texas_value.append(json_data["response"]["data"][i]["value"])
            texas_period.append(json_data["response"]["data"][i]["period"])
    #sort data
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
    max_value = max(texas_value)
    return render_template('layout.html', start = start, end = end, selecttype = selecttype, states = states, title= title, max=max_value//10, labels=texas_period, values=texas_value)

@app.route("/news")
def news():
    news_api = "https://newsapi.org/v2/everything?q=petroleum&from=2022-10-30&sortBy=relevency&apiKey=85ced64dc13d4ac3b1084221bf8ffd47"
    response = requests.get(news_api)
    json_data = json.loads(response.text)
    news_source = []
    news_headline = []
    news_author = []
    news_description = []
    news_url = []
    news_img = []

    for i in range(4):
        news_source.append(json_data["articles"][i]['source']['name'])
        news_headline.append(json_data["articles"][i]['title'])
        news_author.append(json_data["articles"][i]['author'])
        news_description.append(json_data["articles"][i]['description'])
        news_url.append(json_data["articles"][i]['url'])
        news_img.append(json_data["articles"][i]['urlToImage'])

    
    
    
    return render_template("news.html", news_source = news_source, news_headline = news_headline, news_url = news_url, news_author = news_author, news_description = news_description, news_img = news_img)

if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
