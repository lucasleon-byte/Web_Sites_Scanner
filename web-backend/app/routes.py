from flask import Blueprint, request, jsonify, current_app
from bson import json_util
import json
import time
from zapv2 import ZAPv2

main = Blueprint('main', __name__)

ZAP_API_KEY = 'diplomskiRad_Aplikacija'  
ZAP_ADDRESS = 'http://127.0.0.1'
ZAP_PORT = '8080'
zap = ZAPv2(apikey=ZAP_API_KEY, proxies={'http': f'{ZAP_ADDRESS}:{ZAP_PORT}', 'https': f'{ZAP_ADDRESS}:{ZAP_PORT}'})

@main.route('/scan', methods=['POST'])
def scan():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    target_url = data.get('url')

    if not target_url:
        return jsonify({'error': 'No URL provided'}), 400

    collection = current_app.db['results']
    collection.create_index('url')

    existing_result = collection.find_one({'url': target_url}, {'alerts': 1})

    if existing_result:
        existing_alerts = existing_result['alerts']
        return jsonify({
            'message': f'This URL has already been scanned. Do you want to scan it again?',
            'alert_types': list(existing_alerts.keys()),
            'new_scan_url': f'/scan_again?url={target_url}'
        }), 200

    zap.urlopen(target_url)
    time.sleep(2)

    scan_id = zap.spider.scan(target_url)
    time.sleep(2)

    while int(zap.spider.status(scan_id)) < 100:
        time.sleep(2)
        
    # Start Active Scan 
    # scan_id = zap.ascan.scan(target_url)
    # while int(zap.ascan.status(scan_id)) < 100:
    #   time.sleep(5) 

    alerts = zap.core.alerts(baseurl=target_url)
    grouped_alerts = {}
    for alert in alerts:
        alert_type = alert['alert']
        if alert_type not in grouped_alerts:
            grouped_alerts[alert_type] = []
        grouped_alerts[alert_type].append(alert)

    result_id = collection.insert_one({
        'url': target_url,
        'alerts': json.loads(json_util.dumps(grouped_alerts)),
        'timestamp': time.time()
    }).inserted_id

    return jsonify({'id': str(result_id), 'alert_types': list(grouped_alerts.keys())}), 200

@main.route('/scan_again', methods=['POST'])
def scan_again():
    target_url = request.args.get('url')

    if not target_url:
        return jsonify({'error': 'No URL provided'}), 400

    collection = current_app.db['results']
    collection.delete_one({'url': target_url})

    zap.urlopen(target_url)
    time.sleep(2)

    scan_id = zap.spider.scan(target_url)
    time.sleep(2)

    while int(zap.spider.status(scan_id)) < 100:
        time.sleep(2)

    alerts = zap.core.alerts(baseurl=target_url)
    grouped_alerts = {}
    for alert in alerts:
        alert_type = alert['alert']
        if alert_type not in grouped_alerts:
            grouped_alerts[alert_type] = []
        grouped_alerts[alert_type].append(alert)

    result_id = collection.insert_one({
        'url': target_url,
        'alerts': json.loads(json_util.dumps(grouped_alerts)),
        'timestamp': time.time()
    }).inserted_id

    return jsonify({'id': str(result_id), 'alert_types': list(grouped_alerts.keys())}), 200

@main.route('/results', methods=['GET'])
def get_results():
    collection = current_app.db['results']
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    documents = collection.find().skip((page - 1) * per_page).limit(per_page)
    result = [json.loads(json_util.dumps(doc)) for doc in documents]
    return jsonify(result)

@main.route('/alerts', methods=['GET'])
def list_alert_types():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    collection = current_app.db['results']
    result = collection.find_one({'url': url}, {'alerts': 1})

    if not result:
        return jsonify({'error': 'No scan results found for this URL'}), 404

    grouped_alerts = result['alerts']
    alert_types = list(grouped_alerts.keys())

    return jsonify({'alert_types': alert_types}), 200

@main.route('/alerts/<alert_type>', methods=['GET'])
def get_alert_details(alert_type):
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    collection = current_app.db['results']
    result = collection.find_one({'url': url}, {'alerts': 1})

    if not result:
        return jsonify({'error': 'No scan results found for this URL'}), 404

    grouped_alerts = result['alerts']

    if alert_type not in grouped_alerts:
        return jsonify({'error': f'No alerts of type {alert_type} found'}), 404

    alert_details = grouped_alerts[alert_type]

    return jsonify({'alert_type': alert_type, 'details': alert_details}), 200
