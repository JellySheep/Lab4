#!/usr/bin/env python3
import json
import subprocess
import psycopg2
import uuid
import os
import sys
from datetime import datetime

def main():
    # Пути
    sbom_file = "./sbom.cdx.json"
    os_id_path = "/etc/machine-id"

    # 1. ID системы
    if os.path.exists(os_id_path):
        with open(os_id_path, "r") as f:
            os_id = f.read().strip()
    else:
        os_id = str(uuid.uuid4())

    os_name = "Debian GNU/Linux 12 (bookworm)"

    # 2. Запуск CdxGen
    print("--- Запуск сканирования ---")
    res = subprocess.run(["cdxgen", "-t", "os", "-o", sbom_file, "/"])

    if res.returncode != 0:
        print("Ошибка: cdxgen упал! Проверь права или наличие пакета.")
        sys.exit(1)

    # Вставка патча: принудительная смена версии спецификации с 1.7 на 1.5
    try:
        with open(sbom_file, 'r') as f:
            content = f.read()
        content = content.replace('"specVersion":"1.7"', '"specVersion":"1.5"')
        with open(sbom_file, 'w') as f:
            f.write(content)
    except Exception as e:
        print(f"Ошибка при патче версии SBOM: {e}")
        sys.exit(1)

    # 3. Парсинг
    try:
        with open(sbom_file, "r") as f:
            sbom = json.load(f)
            components = sbom.get("components", [])
            sw_list = [{"name": c.get("name"), "version": c.get("version")} for c in components]
            software_count = len(components)
    except Exception as e:
        print(f"Ошибка чтения JSON: {e}")
        sys.exit(1)

    # 4. БД
    try:
        conn = psycopg2.connect("dbname=monitoring user=user password=password host=localhost port=5432")
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO os_inventory (os_id, os_name, software_count, software_list, collected_at)
               VALUES (%s, %s, %s, %s, %s)""",
            (os_id, os_name, software_count, json.dumps(sw_list), datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[{datetime.now()}] Успех: {software_count} пакетов в базе.")
    except Exception as e:
        print(f"Ошибка БД: {e}")

if __name__ == "__main__":
    main()
