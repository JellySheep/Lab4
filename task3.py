#!/usr/bin/env python3
import json
import psycopg2
from datetime import datetime

def get_severity(vuln):
    # Проверяем массив database_specific
    if "database_specific" in vuln and "severity" in vuln["database_specific"]:
        return vuln["database_specific"]["severity"]
    # Проверяем массив severity (CVSS)
    if "severity" in vuln and len(vuln["severity"]) > 0:
        return vuln["severity"][0].get("type", "UNKNOWN")
    return "UNKNOWN"

def main():
    scan_file = "./scan.json"

    try:
        conn = psycopg2.connect("dbname=monitoring user=user password=password host=localhost port=5432")
        cur = conn.cursor()

        # 1. Получаем ID последней записи об ОС, чтобы связать с ней уязвимости
        cur.execute("SELECT id FROM os_inventory ORDER BY collected_at DESC LIMIT 1;")
        os_record = cur.fetchone()
        os_inv_id = os_record[0] if os_record else None

        # 2. Читаем результаты сканера
        with open(scan_file, "r") as f:
            data = json.load(f)

            results = data.get("results", [])
            vuln_count = 0

            # Исправленная вложенность под формат osv-scanner:
            for result_item in results:
                packages = result_item.get("packages", [])
                
                for pkg_info in packages:
                    package = pkg_info.get("package", {})
                    pkg_name = package.get("name", "Unknown")
                    pkg_version = package.get("version", "Unknown")

                    for vuln in pkg_info.get("vulnerabilities", []):
                        vuln_id = vuln.get("id", "UNKNOWN-ID")
                        summary = vuln.get("summary", "No description available")
                        severity = get_severity(vuln)

                        # 3. Пишем в твою таблицу
                        cur.execute(
                            """INSERT INTO vulnerabilities
                               (os_inventory_id, vuln_id, package_name, package_version, severity, summary, found_at)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (os_inv_id, vuln_id, pkg_name, pkg_version, severity, summary, datetime.now())
                        )
                        vuln_count += 1

        conn.commit()
        print(f"[{datetime.now()}] Успех: {vuln_count} уязвимостей записано в БД.")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    main()
