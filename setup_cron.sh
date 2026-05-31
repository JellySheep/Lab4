#!/bin/bash

# Получаем абсолютный путь к текущей директории (/home/artem/lab5)
WORK_DIR="$(cd "$(dirname "$0")" && pwd)"

# Даем права на исполнение основному скрипту пайплайна
chmod +x "$WORK_DIR/run_pipeline.sh"

# Формируем строку задачи для cron (каждые 5 минут)
CRON_JOB="*/5 * * * * $WORK_DIR/run_pipeline.sh >> $WORK_DIR/pipeline.log 2>&1"

# Проверяем, нет ли уже такой задачи в cron, чтобы не дублировать
crontab -l 2>/dev/null | grep -F "$WORK_DIR/run_pipeline.sh" >/dev/null
if [ $? -eq 0 ]; then
    echo "Задача уже добавлена в crontab."
else
    # Добавляем задачу в существующий crontab
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Успех! Задача добавлена в cron на запуск каждые 5 минут."
fi

echo "Текущее расписание cron для пользователя:"
crontab -l
