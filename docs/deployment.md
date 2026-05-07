# Deployment

Przewodnik wdrażania Language Detection Dialog System do produkcji.

## Opcje deploymentu

- [Docker](#docker)
- [Docker Compose](#docker-compose)
- [Systemowe (Linux/Unix)](#linux-systemd)
- [Cloud (Heroku, AWS, GCP)](#cloud)

## Docker

### Budowanie obrazu

```bash
docker build -t language-detection:latest .
```

### Uruchomienie kontenera

```bash
docker run -p 8000:8000 language-detection:latest
```

API będzie dostępne pod: `http://localhost:8000`

### Zaawansowane opcje

Z mapowaniem volumenu (dla logów):

```bash
docker run -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  language-detection:latest
```

Z zmiennymi środowiskowymi:

```bash
docker run -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  -e ASR_MODEL=base \
  language-detection:latest
```

## Docker Compose

### Uruchomienie

```bash
docker-compose up
```

### Zatrzymanie

```bash
docker-compose down
```

### Rebuild

```bash
docker-compose up --build
```

### Uruchomienie w tle

```bash
docker-compose up -d
```

### Logi

```bash
docker-compose logs -f app
```

### Konfiguracja Docker Compose

Plik `docker-compose.yml` definiuje:
- Port: 8000
- Wolumen dla logów
- Konfiguracja sieci

## Linux Systemd

Dla deploymentu na serwerze Linux.

### 1. Tworzenie systemd service file

Utwórz `/etc/systemd/system/language-detection.service`:

```ini
[Unit]
Description=Language Detection Dialog System
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/language-detection
Environment="PATH=/opt/language-detection/venv/bin"
ExecStart=/opt/language-detection/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

### 2. Setup

```bash
# Sklonuj repozytorium
git clone <repo-url> /opt/language-detection
cd /opt/language-detection

# Utwórz venv
python3 -m venv venv
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Ustaw uprawnienia
sudo chown -R www-data:www-data /opt/language-detection
```

### 3. Włączenie i start

```bash
sudo systemctl daemon-reload
sudo systemctl enable language-detection
sudo systemctl start language-detection

# Sprawdzenie statusu
sudo systemctl status language-detection
```

### 4. Monitoring

```bash
# Logi w real-time
sudo journalctl -u language-detection -f

# Ostatnie 100 linii
sudo journalctl -u language-detection -n 100
```

## Nginx Reverse Proxy

Dla produkcji rekomenduję użycie Nginx jako reverse proxy.

### Konfiguracja Nginx

Utwórz `/etc/nginx/sites-available/language-detection`:

```nginx
upstream language_detection {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://language_detection;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (jeśli będzie potrzebny)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Włączenie

```bash
sudo ln -s /etc/nginx/sites-available/language-detection \
           /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx
```

### HTTPS (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d api.example.com
```

## Cloud Deployments

### Heroku

#### 1. Inicjalizacja

```bash
# Zainstaluj Heroku CLI
brew tap heroku/brew && brew install heroku

# Login
heroku login

# Utwórz aplikację
heroku create my-language-detection
```

#### 2. Deployment

```bash
git push heroku main
```

#### 3. Monitoring

```bash
heroku logs --tail
```

### AWS (Elastic Beanstalk)

#### 1. Setup

```bash
pip install awsebcli
eb init
```

#### 2. Deployment

```bash
eb create
eb deploy
```

### Google Cloud (App Engine)

#### 1. Konfiguracja

Utwórz `app.yaml`:

```yaml
runtime: python310

env: standard

handlers:
- url: /.*
  script: auto

manual_scaling:
  instances: 1
```

#### 2. Deployment

```bash
gcloud app deploy
```

## Production Checklist

- [ ] **Zmienne środowiskowe**: Ustaw `ENVIRONMENT=production`
- [ ] **Logging**: Włącz proper logging do pliku/serwisu
- [ ] **CORS**: Dostosuj do Twojego domenu
- [ ] **Rate Limiting**: Rozważ dodanie limitów
- [ ] **SSL/TLS**: Użyj HTTPS
- [ ] **Backups**: Utwórz backup plan
- [ ] **Monitoring**: Setup alertów
- [ ] **Health Checks**: Zonfiguruj health checks
- [ ] **Load Balancing**: Jeśli potrzebny - użyj load balancer
- [ ] **Graceful Shutdown**: Setup proper shutdown handling

## Zmienne środowiskowe

```bash
# .env.production
ASR_MODEL=base
LOG_LEVEL=INFO
WORKERS=4
ENVIRONMENT=production
```

## Performance Tuning

### Ustawienia Uvicorn

```bash
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --loop uvloop \
  --http httptools
```

### Caching

Włącz caching w Nginx:

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;

location /detect-language/text {
    proxy_cache my_cache;
    proxy_cache_valid 200 10m;
    proxy_pass http://language_detection;
}
```

## Monitoring i Logging

### Logowanie

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='/var/log/language-detection/app.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Monitoring

```bash
# Cron job dla health checks
*/5 * * * * curl -f http://localhost:8000/health || systemctl restart language-detection
```

### Prometheus Metrics (opcjonalnie)

```bash
pip install prometheus-client
```

## Updating w Production

### Blue-Green Deployment

```bash
# Deploy na nowy instans
docker run -d --name language-detection-new language-detection:v2

# Test
curl http://localhost:8001/health

# Switch traffic
docker stop language-detection
docker rename language-detection-new language-detection
```

### Zero-downtime Updates

Używając systemd:

```bash
# Deploy
git pull
pip install -r requirements.txt

# Reload
sudo systemctl reload language-detection
```

## Troubleshooting

### Problem: OOM (Out of Memory)

```bash
# Zwiększ pamięć kontenera
docker run -m 4g language-detection:latest
```

### Problem: ASR model nie ładuje się

```bash
# Pre-download modelu
docker build --build-arg ASR_MODEL=base .
```

### Problem: Port już w użyciu

```bash
# Użyj innego portu
docker run -p 9000:8000 language-detection:latest
```

## Backup Strategy

```bash
# Backup logs i modeli
tar -czf backup-$(date +%Y%m%d).tar.gz \
  /var/log/language-detection/ \
  ~/.cache/whisper/
```

## Skalowanie

Dla wysokiego traffic:

1. **Horizontal Scaling**: Multiple instances
2. **Load Balancing**: Nginx, HAProxy
3. **Caching**: Redis dla cache
4. **Database**: Jeśli będzie historia - PostgreSQL
5. **Queues**: Celery dla async tasks

```bash
# Docker scaling
docker-compose up -d --scale app=3
```

## Support i Dokumentacja

- [FastAPI Production Guidelines](https://fastapi.tiangolo.com/deployment/concepts/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
