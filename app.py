from flask import Flask, request, Response
import os
import requests
import json

app = Flask(__name__)

BROWSERLESS_API_KEY = os.environ.get('BROWSERLESS_API_KEY')

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return {'error': 'Missing url parameter'}, 400
    if 'ffecompet.ffe.com' not in url:
        return {'error': 'Only ffecompet.ffe.com URLs allowed'}, 403
    try:
        # Utilise Browserless pour lancer un vrai Chrome
        response = requests.post(
            f'https://production-sfo.browserless.io/content?token={BROWSERLESS_API_KEY}',
            headers={'Content-Type': 'application/json'},
            json={
                'url': url,
                'waitForSelector': 'table',
                'rejectResourceTypes': ['image', 'font', 'stylesheet'],
            },
            timeout=30
        )
        if response.status_code != 200:
            return {'error': f'Browserless error: {response.status_code}'}, response.status_code
        return Response(
            response.text,
            status=200,
            mimetype='text/html',
            headers={'Access-Control-Allow-Origin': '*'}
        )
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/')
def index():
    return {'service': 'FFE Watcher Proxy', 'status': 'running'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
