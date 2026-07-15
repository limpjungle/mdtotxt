# MD to TXT Converter

Веб-приложение на Flask для конвертации Markdown-файлов в чистый текст.  
Принимает `.md` через форму или API, возвращает `.txt` без форматирования.  
В комплекте - сборка Docker, docker-compose с Prometheus, Grafana и Node Exporter для мониторинга.

## Возможности

- Конвертация Markdown в обычный текст с сохранением структуры.
- Веб-интерфейс: загрузка файла через браузер.
- HTTP API: `POST /convert` с multipart/form-data.
- Полная контейнеризация (Docker).
- Готовый мониторинг: Prometheus собирает метрики Flask и хоста, Grafana визуализирует.

## Требования

- Docker
- Docker Compose (версия 1.27+)

## Быстрый старт

1. Склонируйте репозиторий:
   ```bash
   git clone github.com/limpjungle/mdtotxt/
   cd mdtotxt
Запустите все сервисы:

```bash
docker-compose up -d
```
Откройте в браузере:

Веб-интерфейс: http://localhost:5000

Prometheus: http://localhost:9090

Grafana: http://localhost:3000 (admin:admin)

## Использование API

```bash
curl -F "file=@document.md" http://localhost:5000/convert -o result.txt
```
## Мониторинг
Все метрики автоматически собираются в Prometheus и отображаются в Grafana.

Метрики Flask: количество запросов, время ответа, коды статусов — доступны на /metrics приложения.

Метрики хоста: CPU, память, диск, сеть — через Node Exporter.

Готовые дашборды Grafana:

Flask App Monitoring(ID: 10856)

Node Exporter Full(ID: 1860)
