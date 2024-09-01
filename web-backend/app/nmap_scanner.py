import nmap
import socket
from flask import jsonify
from bson import json_util
import time
from flask import current_app

nm = nmap.PortScanner()

def resolve_hostname_to_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.error as e:
        raise ValueError(f"Unable to resolve hostname {hostname}: {str(e)}")

def perform_nmap_scan(target_ip):
    try:
        nm.scan(hosts=target_ip, arguments='-T4 -F')
        return nm.csv()
    except Exception as e:
        raise RuntimeError(f'Failed to perform scan: {e}')

def nmap_scan(target_url):
    collection = current_app.db['nmap_results']
    target_url = target_url.replace('http://', '').replace('https://', '')
    existing_result = collection.find_one({'url': target_url})

    if existing_result:
        return {
            'message': f'This URL has already been scanned. Do you want to scan it again?',
            'id': str(existing_result['_id']),
            'scan_data': existing_result['scan_data'],
            'new_scan_url': f'/nmap_scan_again?url={target_url}'
        }, 200

    try:
        target_ip = resolve_hostname_to_ip(target_url)
        scan_data = perform_nmap_scan(target_ip)
    except (ValueError, RuntimeError) as e:
        return jsonify({'error': str(e)}), 400

    result_id = collection.insert_one({
        'url': target_url,
        'ip': target_ip,
        'scan_data': scan_data,
        'timestamp': time.time()
    }).inserted_id

    return {'id': str(result_id), 'scan_data': scan_data}, 200

def nmap_scan_again(target_url):
    collection = current_app.db['nmap_results']
    target_url = target_url.replace('http://', '').replace('https://', '')
    collection.delete_one({'url': target_url})

    try:
        target_ip = resolve_hostname_to_ip(target_url)
        scan_data = perform_nmap_scan(target_ip)
    except (ValueError, RuntimeError) as e:
        return jsonify({'error': str(e)}), 400

    result_id = collection.insert_one({
        'url': target_url,
        'ip': target_ip,
        'scan_data': scan_data,
        'timestamp': time.time()
    }).inserted_id

    return {'id': str(result_id), 'scan_data': scan_data}, 200
