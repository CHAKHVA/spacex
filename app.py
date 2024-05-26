import os
from dotenv import load_dotenv
from datetime import datetime


from flask import Flask, render_template
import requests

load_dotenv()

app = Flask(__name__)
app.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))


def fetch_launches():
    response = requests.get("https://api.spacexdata.com/v5/launches")
    if response.status_code != 200:
        return []

    return response.json()


def categorize_launches(launches):
    successful = list(filter(lambda x: x["success"], launches))
    failed = list(filter(lambda x: not x["success"], launches))
    upcoming = list(filter(lambda x: x["upcoming"], launches))

    return {"successful": successful, "failed": failed, "upcoming": upcoming}


launches = categorize_launches(fetch_launches())


@app.template_filter("date_only")
def date_only_filter(dt):
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ").date()


@app.route("/")
def index():
    return render_template("index.html", launches=launches, enumerate=enumerate)


if __name__ == "__main__":
    app.run(debug=True)
