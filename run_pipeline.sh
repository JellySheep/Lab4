#!/bin/bash

cd "$(dirname "$0")"

echo "[$(date)] --- СТАРТ КОНВЕЙЕРА СКАНИРОВАНИЯ ---"

python3 task2.py

if [ ! -f "./sbom.cdx.json" ]; then
    echo "[$(date)] Ошибка: Файл sbom.cdx.json не найден. Прерывание."
    exit 1
fi

echo "[$(date)] Запуск osv-scanner..."
./osv-scanner --sbom=sbom.cdx.json --format=json > scan.json 2>/dev/null

python3 task3.py

echo "[$(date)] --- КОНВЕЙЕР УСПЕШНО ЗАВЕРШЕН ---"
