#!/bin/bash

# Переходим в директорию скрипта, чтобы относительные пути работали из cron
cd "$(dirname "$0")"

echo "[$(date)] --- СТАРТ КОНВЕЙЕРА СКАНИРОВАНИЯ ---"

# Шаг 1: Запуск инвентаризации ОС и софта (cdxgen + отправка в БД)
python3 task2.py

# Проверка, создался ли файл sbom.cdx.json
if [ ! -f "./sbom.cdx.json" ]; then
    echo "[$(date)] Ошибка: Файл sbom.cdx.json не найден. Прерывание."
    exit 1
fi

# Шаг 2: Генерация scan.json через локальный бинарник osv-scanner
echo "[$(date)] Запуск osv-scanner..."
./osv-scanner --sbom=sbom.cdx.json --format=json > scan.json 2>/dev/null

# Шаг 3: Парсинг уязвимостей и отправка в БД
python3 task3.py

echo "[$(date)] --- КОНВЕЙЕР УСПЕШНО ЗАВЕРШЕН ---"
