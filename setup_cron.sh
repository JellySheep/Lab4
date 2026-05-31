#!/bin/bash

WORK_DIR="$(cd "$(dirname "$0")" && pwd)"

chmod +x "$WORK_DIR/run_pipeline.sh"

CRON_JOB="*/5 * * * * $WORK_DIR/run_pipeline.sh >> $WORK_DIR/pipeline.log 2>&1"

crontab -l 2>/dev/null | grep -F "$WORK_DIR/run_pipeline.sh" >/dev/null
if [ $? -eq 0 ]; then
    echo "Задача уже добавлена в crontab."
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Успех! Задача добавлена в cron на запуск каждые 5 минут."
fi

echo "Текущее расписание cron для пользователя:"
crontab -l
