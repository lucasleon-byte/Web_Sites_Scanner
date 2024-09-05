import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VIRUSTOTAL_API_KEY = '2485b753e49426f5a1916993ae38b4bffe4dc22a84248b6461409024c09c7f6a'
VIRUSTOTAL_API_URL = 'https://www.virustotal.com/api/v3/urls'

def perform_virustotal_scan(target_url):
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = f"url={target_url}"

    print(f"Performing VirusTotal scan for URL: {target_url}")
    print(f"Request URL: {VIRUSTOTAL_API_URL}")
    print(f"Request Headers: {headers}")
    print(f"Request Data: {data}")

    try:
        response = requests.post(VIRUSTOTAL_API_URL, headers=headers, data=data)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Exception Occurred: {e}")
        raise RuntimeError(f'Failed to perform VirusTotal scan: {e}')

@app.route('/scan', methods=['POST'])
def scan_url():
    data = request.get_json()
    target_url = data.get('url')
    
    if not target_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        result = perform_virustotal_scan(target_url)
        return jsonify(result), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/analysis/<analysis_id>', methods=['GET'])
def get_analysis_results(analysis_id):
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
