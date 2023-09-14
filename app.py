import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template
import requests

app = Flask(__name__)
app.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))


def fetch_launches():
    response = requests.get("https://api.spacexdata.com/v5/launches")
    if response.status_code != 200:
        return []

    return response.json()


def categorize_launches(launches):
    successful = list(filter(lambda x: x["success"] == True, launches))
    failed = list(filter(lambda x: x["success"] == False, launches))
    upcoming = list(filter(lambda x: x["upcoming"] == True, launches))

    return {"successful": successful, "failed": failed, "upcoming": upcoming}


launches = categorize_launches(fetch_launches())


@app.route("/")
def index():
    return render_template("index.html", launches=launches)


if __name__ == "__main__":
    app.run(debug=True)
