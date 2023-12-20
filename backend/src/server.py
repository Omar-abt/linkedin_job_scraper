from flask import Flask, request, jsonify
import subprocess
import os


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return "<p>Test</p>"

@app.route("/scraper", methods=['POST'])
def scraper():
    # data = request.json  # For JSON payload
    # data = request.form  # For form data

    print(os.getcwd())

    job_name = request.form.get("job_name")
    job_location = request.form.get("job_location")

    subprocess.run(['python3', 'backend/src/scraper/scraper.py', job_name, job_location])