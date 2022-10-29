from flask import Flask, render_template
import requests
import json
api_key = "lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3"
response = requests.get("https://api.eia.gov/v2/natural-gas/prod/oilwells/data/?api_key=lLhgwKk3K0bBy3WCT8kUPbNErsjjRcJjO8h5ZUs3")

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent= 4)
    print(text)

jprint(response.json())
print(response.status_code)
# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "<p>Hello<p>"

# if __name__ == "__main__":
#     app.run()