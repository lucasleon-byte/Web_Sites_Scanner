import requests
import time
from flask import jsonify, current_app

VIRUSTOTAL_API_KEY = 'YOUR_VIRUSTOTAL_API_KEY'
VIRUSTOTAL_API_URL = 'https://www.virustotal.com/api/v3/urls'

def perform_virustotal_scan(target_url):
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY,
        'Content-Type': 'application/json'
    }

    # Encode URL to base64
    url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")

    try:
        response = requests.post(VIRUSTOTAL_API_URL, headers=headers, json={"url": target_url})
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f'Failed to submit URL for scanning: {response.status_code} {response.text}')
    except Exception as e:
        raise RuntimeError(f'Failed to perform VirusTotal scan: {e}')

def get_virustotal_report(url_id):
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY
    }

    try:
        response = requests.get(f'{VIRUSTOTAL_API_URL}/{url_id}', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f'Failed to retrieve report: {response.status_code} {response.text}')
    except Exception as e:
        raise RuntimeError(f'Failed to retrieve VirusTotal report: {e}')

def virustotal_scan(target_url):
    collection = current_app.db['virustotal_results']
    url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
    
    existing_result = collection.find_one({'url': target_url})

    if existing_result:
        return {
            'message': f'This URL has already been scanned. Do you want to scan it again?',
            'id': str(existing_result['_id']),
            'scan_data': existing_result['scan_data'],
            'new_scan_url': f'/virustotal_scan_again?url={target_url}'
        }, 200

    try:
        scan_data = perform_virustotal_scan(target_url)
        result_id = collection.insert_one({
            'url': target_url,
            'scan_data': scan_data,
            'timestamp': time.time()
        }).inserted_id

        return {'id': str(result_id), 'scan_data': scan_data}, 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 400

def virustotal_scan_again(target_url):
    collection = current_app.db['virustotal_results']
    url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
    collection.delete_one({'url': target_url})

    try:
        scan_data = perform_virustotal_scan(target_url)
        result_id = collection.insert_one({
            'url': target_url,
            'scan_data': scan_data,
            'timestamp': time.time()
        }).inserted_id

        return {'id': str(result_id), 'scan_data': scan_data}, 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 400
