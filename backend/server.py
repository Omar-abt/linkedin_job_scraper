from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


@app.route("/")
def hello_world():
    return ("<p>LinkedIn Job Scraper API</p>"
            "<p>To Access the scraper use the 'scraper' endpoint</p>")

@app.route("/test")
def test():
    return "<p>Test</p>"

@app.route("/scraper", methods=['POST'])
def scraper():
    # data = request.json  # For JSON payload
    # data = request.form  # For form data

    data = request.json
    if data:
        job_name = data.get("job_name")
        job_location = data.get("job_location")
    else:
        return jsonify({'error': 'Invalid JSON data'}), 400


    try:
        subprocess.run(['python3', 'src/scraper/scraper.py', job_name, job_location])
        return jsonify({'message': 'Script executed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()