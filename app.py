import os
from dotenv import load_dotenv
import pprint

load_dotenv()

from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)
app.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))


def fetch_launches():
    response = requests.get("https://api.spacexdata.com/v5/launches")
    if response.status_code != 200:
        return []

    return response.json()


def categorize_launches(launches):
    upcoming = filter(lambda x: x["upcoming"] == True, launches)
    successful = filter(lambda x: x["success"] == True, launches)
    failed = filter(lambda x: x["success"] == False, launches)

    return upcoming, successful, failed


@app.route("/")
def index():
    launches = categorize_launches(fetch_launches())
    pprint.pprint(launches)

    return render_template("index.html", launches=launches)


if __name__ == "__main__":
    app.run(debug=True)
