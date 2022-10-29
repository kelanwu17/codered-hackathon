from flask import Flask, render_template
import requests
import json
api_key = "lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3"
response = requests.get("https://api.eia.gov/v2/natural-gas/prod/wells/data/?api_key=" + api_key + "&data[]=value")

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent= 4)
    print(text)

json_data = json.loads(response.text)
jprint(json_data["response"]["data"][0])


# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.run()