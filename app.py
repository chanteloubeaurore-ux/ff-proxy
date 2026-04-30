flask==3.0.0
cloudscraper==1.2.71
gunicorn==21.2.0
        
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
