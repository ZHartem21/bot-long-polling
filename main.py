import requests
import os
import telegram

from dotenv import load_dotenv
from textwrap import dedent
from time import sleep


USER_REVIEWS_LONG_POLLING = 'https://dvmn.org/api/long_polling/'


def main():
    load_dotenv('.env')
    dvmn_token = os.environ['DVMN_TOKEN']
    tg_token = os.environ['TG_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=tg_token)
    headers = {'Authorization': 'Token {0}'.format(dvmn_token)}
    timestamp = None
    while True:
        try:
            if timestamp:
                response = requests.get(USER_REVIEWS_LONG_POLLING, headers=headers, timeout=90, params={'Timestamp': timestamp})
            else:
                response = requests.get(USER_REVIEWS_LONG_POLLING, headers=headers, timeout=90,)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            continue
        except ConnectionError:
            sleep(30)
            continue
        review = response.json()
        last_review = review['new_attempts'][0]
        timestamp = last_review['timestamp']
        if last_review['is_negative'] and review['status'] == 'found':
            message_text = dedent(f'''\
                У вас проверили работу "{last_review['lesson_title']}".\n
                К сожалению, в работе нашлись ошибки.\n
                Ссылка на урок: {last_review['lesson_url']}''')
            bot.send_message(text=message_text, chat_id=tg_chat_id)
        if not last_review['is_negative']:
            message_text = dedent(f'''\
                У вас проверили работу "{last_review['lesson_title']}".\n
                Преподавателю всё понравилось, можно приступать к следующему уроку!\n
                Ссылка на урок: {last_review['lesson_url']}''')
            bot.send_message(text=message_text, chat_id=tg_chat_id)


if __name__ == '__main__':
    main()
