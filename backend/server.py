from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)


@app.route("/")
def main():
    return ("<h2>LinkedIn Job Scraper API</h2>"
            "<p>To Access the scraper use the '/scraper' endpoint</p>")

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
        output_file = "./output/jobs_cleaned.csv"

        if os.path.exists(output_file):
            return send_file(output_file, as_attachment=True)
        else:
            raise FileNotFoundError
        # return jsonify({'message': 'Script executed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()