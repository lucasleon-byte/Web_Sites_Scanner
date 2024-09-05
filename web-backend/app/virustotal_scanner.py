import requests
import time
from flask import current_app

VIRUSTOTAL_API_KEY = '2485b753e49426f5a1916993ae38b4bffe4dc22a84248b6461409024c09c7f6a'
VIRUSTOTAL_API_URL = 'https://www.virustotal.com/api/v3/urls'

def perform_virustotal_scan(target_url):
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    
    data = f"url={target_url}"
    
    try:
        response = requests.post(VIRUSTOTAL_API_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Failed to perform VirusTotal scan: {e}')

def virustotal_scan(target_url):
    collection = current_app.db['virustotal_results']
    target_url = target_url.replace('http://', '').replace('https://', '')
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
    except RuntimeError as e:
        return {'error': str(e)}, 400

    result_id = collection.insert_one({
        'url': target_url,
        'scan_data': scan_data,
        'timestamp': time.time()
    }).inserted_id

    return {'id': str(result_id), 'scan_data': scan_data}, 200

def virustotal_scan_again(target_url):
    collection = current_app.db['virustotal_results']
    target_url = target_url.replace('http://', '').replace('https://', '')
    collection.delete_one({'url': target_url})

    try:
        scan_data = perform_virustotal_scan(target_url)
    except RuntimeError as e:
        return {'error': str(e)}, 400

    result_id = collection.insert_one({
        'url': target_url,
        'scan_data': scan_data,
        'timestamp': time.time()
    }).inserted_id

    return {'id': str(result_id), 'scan_data': scan_data}, 200

def get_analysis_results(analysis_id):
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Failed to fetch analysis results: {e}')
