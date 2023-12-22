import requests

# URL of your Flask endpoint
url = 'http://127.0.0.1:8000//scraper'  # Replace with your Flask server URL

# Data to be sent to the endpoint
data = {
    'job_name': 'Software Engineer',
    'job_location': 'Ottawa'
}

# Make a POST request to the Flask endpoint
response = requests.post(url, data=data)

# Print the response
print(response.text)
