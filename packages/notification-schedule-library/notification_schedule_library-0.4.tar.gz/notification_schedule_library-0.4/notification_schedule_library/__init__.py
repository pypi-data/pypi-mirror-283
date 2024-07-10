import os
import requests
import json

# Fetch API URLs and tokens from environment variables
API_URL = os.getenv('NOTIFICATION_API_URL')
ACCESS_TOKEN = os.getenv('NOTIFICATION_ACCESS_TOKEN')
WEBHOOK_TOKEN = os.getenv('NOTIFICATION_WEBHOOK_TOKEN')


def print_variables():
    print(f"{API_URL}\n{ACCESS_TOKEN}\n{WEBHOOK_TOKEN}")

def create_rule(data):
    url = f"{API_URL}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }
    data['token'] = WEBHOOK_TOKEN
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json(), response.status_code

def delete_rule(rule_id):
    url = f"{API_URL}{rule_id}"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }
    response = requests.delete(url, headers=headers)
    return response.status_code

def update_rule(rule_id, data):
    url = f"{API_URL}{rule_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }
    data['token'] = WEBHOOK_TOKEN
    response = requests.put(url, data=json.dumps(data), headers=headers)
    return response.json(), response.status_code
