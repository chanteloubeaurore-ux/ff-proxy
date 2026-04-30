# FFE Watcher Proxy

Serveur proxy pour FFE Watcher - contourne la protection Cloudflare de ffecompet.ffe.com

## Déploiement sur Render

1. Créez un compte sur render.com
2. New > Web Service > connectez ce repo GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Plan: Free

## Usage

`GET /fetch?url=https://ffecompet.ffe.com/concours/202622022`
