# Системные зависимости (устанавливаются в ОС):
1. Node.js LTS: curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs
2. sudo apt-get install -y nodejs python3-pip python3-psycopg2
3. sudo npm install -g @cyclonedx/cdxgen
4. pip3 install -r requirements.txt
5. wget https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_amd64 -O osv-scanner && chmod +x osv-scanner

#Запуск конвейера

```bash
docker-compose up -d
```

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

###тестовый запуск
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

Grafana: http://localhost:3000 (Вход: admin / admin).
Prometheus: http://localhost:9090 (Метрики: os_software_metrics и os_vulnerabilities_metrics).
