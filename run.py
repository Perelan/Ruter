import json, requests
import time
from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

def fetch():
    url = "http://reisapi.ruter.no/StopVisit/GetDepartures/3010370"
    params = dict(
        transporttypes='Metro',
    )

    resp = requests.get(url = url, params = params)
    data = json.loads(resp.text)
    pkg  = []

    for line, i in enumerate(data):
        # Unwrap the dict. and get the data.
        for key, value in i["MonitoredVehicleJourney"].items():
            # Remove un-monitored travels
            if key == "Monitored" and value == False:
                data.remove(i)
                break           # No more needed data from this object

        pkg.append(i["MonitoredVehicleJourney"])

    return pkg

@app.route("/")
def home():
    return render_template('template.html', my_list=fetch())

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug="True")
