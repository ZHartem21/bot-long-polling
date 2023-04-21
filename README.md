# bot-long-polling
 
Скрипт использующий long polling для проверки статуса работ и оповещения ученика при помощи бота телеграм.

## Запуск

Для запуска у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите скрипт командой `python main.py`

## Переменные окружения

Настройки скрипта берутся из переменных окружения. Чтобы их определить, создайте файл `.env` в папке скрипта и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

**Для запуска проекта требуются три переменные**:
- `DVMN_TOKEN` — токен доступа ученика Devman.
- `TG_TOKEN` — токен телеграм бота.
- `TG_CHAT_ID` — id вашего чата с ботом.

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).