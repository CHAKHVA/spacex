import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)
app.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))


def fetch_launches():
    response = requests.get("https://api.spacexdata.com/v4/launches")
    if response.status_code != 200:
        return []

    return response.json()


print(fetch_launches()[0])


@app.route("/")
def index():
    return render_template("index.html", launches=None)


if __name__ == "__main__":
    app.run(debug=True)
