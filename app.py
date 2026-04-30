from flask import Flask, request, jsonify
import requests
import time
import random

app = Flask(__name__)

# Headers qui imitent un vrai navigateur
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-cache',
    'Referer': 'https://ffecompet.ffe.com/',
}

# Session persistante (comme un vrai navigateur)
session = requests.Session()
session.headers.update(BROWSER_HEADERS)

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400
    
    # Sécurité : on accepte uniquement les URLs FFE
    if 'ffecompet.ffe.com' not in url:
        return jsonify({'error': 'Only ffecompet.ffe.com URLs allowed'}), 403
    
    try:
        # Petite pause aléatoire pour paraître humain
        time.sleep(random.uniform(0.5, 1.5))
        
        resp = session.get(url, timeout=15, allow_redirects=True)
        
        # Si Cloudflare bloque, on retente une fois
        if resp.status_code == 403 or 'Vérification de sécurité' in resp.text or 'checking your browser' in resp.text.lower():
            time.sleep(random.uniform(2, 4))
            resp = session.get(url, timeout=15, allow_redirects=True)
        
        return app.response_class(
            response=resp.text,
            status=resp.status_code,
            mimetype='text/html',
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
            }
        )
    except requests.Timeout:
        return jsonify({'error': 'Timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'FFE Proxy'})

@app.route('/')
def index():
    return jsonify({
        'service': 'FFE Watcher Proxy',
        'status': 'running',
        'usage': '/fetch?url=https://ffecompet.ffe.com/concours/XXXXXXX'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
