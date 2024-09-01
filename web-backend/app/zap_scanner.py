import time
from flask import jsonify
from bson import json_util
import json
from zapv2 import ZAPv2
from flask import current_app

ZAP_API_KEY = 'diplomskiRad_Aplikacija'
ZAP_ADDRESS = 'http://127.0.0.1'
ZAP_PORT = '8080'
zap = ZAPv2(apikey=ZAP_API_KEY, proxies={'http': f'{ZAP_ADDRESS}:{ZAP_PORT}', 'https': f'{ZAP_ADDRESS}:{ZAP_PORT}'})

def zap_scan(target_url):
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

    return grouped_alerts

def zap_scan_handler(target_url):
    collection = current_app.db['results']
    existing_result = collection.find_one({'url': target_url}, {'alerts': 1})

    if existing_result:
        existing_alerts = existing_result['alerts']
        return {
            'message': f'This URL has already been scanned. Do you want to scan it again?',
            'alert_types': list(existing_alerts.keys()),
            'new_scan_url': f'/scan_again?url={target_url}'
        }, 200

    grouped_alerts = zap_scan(target_url)
    result_id = collection.insert_one({
        'url': target_url,
        'alerts': json.loads(json_util.dumps(grouped_alerts)),
        'timestamp': time.time()
    }).inserted_id

    return {'id': str(result_id), 'alert_types': list(grouped_alerts.keys())}, 200

def zap_scan_again_handler(target_url):
    collection = current_app.db['results']
    collection.delete_one({'url': target_url})

    grouped_alerts = zap_scan(target_url)
    result_id = collection.insert_one({
        'url': target_url,
        'alerts': json.loads(json_util.dumps(grouped_alerts)),
        'timestamp': time.time()
    }).inserted_id

    return {'id': str(result_id), 'alert_types': list(grouped_alerts.keys())}, 200
