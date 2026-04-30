from flask import Flask, request, Response
import cloudscraper
import time
import random

app = Flask(__name__)

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return {'error': 'Missing url parameter'}, 400
    if 'ffecompet.ffe.com' not in url:
        return {'error': 'Only ffecompet.ffe.com URLs allowed'}, 403
    try:
        time.sleep(random.uniform(0.3, 1.0))
        resp = scraper.get(url, timeout=20)
        return Response(resp.text, status=resp.status_code, mimetype='text/html',
            headers={'Access-Control-Allow-Origin': '*'})
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
