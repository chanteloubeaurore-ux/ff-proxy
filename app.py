from flask import Flask, request, Response
import os
import requests

app = Flask(__name__)

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return {'error': 'Missing url parameter'}, 400
    if 'ffecompet.ffe.com' not in url:
        return {'error': 'Only ffecompet.ffe.com URLs allowed'}, 403
    
    api_key = os.environ.get('BROWSERLESS_API_KEY', '')
    if not api_key:
        return {'error': 'API key not configured'}, 500
    
    try:
        response = requests.post(
            f'https://production-sfo.browserless.io/content?token={api_key}',
            headers={'Content-Type': 'application/json'},
            json={
                'url': url,
                'waitForTimeout': 3000,
                'rejectResourceTypes': ['image', 'font', 'stylesheet'],
            },
            timeout=30
        )
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
    key = os.environ.get('BROWSERLESS_API_KEY', '')
    return {'status': 'ok', 'key_configured': bool(key)}

@app.route('/')
def index():
    return {'service': 'FFE Watcher Proxy', 'status': 'running'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
