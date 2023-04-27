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
    while True:
        timestamp = ''
        try:
            response = requests.get(USER_REVIEWS_LONG_POLLING, headers=headers, timeout=90, params={'Timestamp': timestamp})
            response.raise_for_status()
        except requests.exceptions.ReadTimeout or ConnectionError:
            sleep(30)
            continue
        review = response.json()
        if review['new_attempts'][0]['is_negative'] and review['status'] = 'found':
            message_text = dedent(f'''\
                У вас проверили работу "{review['new_attempts'][0]['lesson_title']}".\n
                К сожалению, в работе нашлись ошибки.\n
                Ссылка на урок: {review['new_attempts'][0]['lesson_url']}''')
            bot.send_message(text=message_text, chat_id=tg_chat_id)
        if not review['new_attempts'][0]['is_negative']:
            message_text = dedent(f'''\
                У вас проверили работу "{review['new_attempts'][0]['lesson_title']}".\n
                Преподавателю всё понравилось, можно приступать к следующему уроку!\n
                Ссылка на урок: {review['new_attempts'][0]['lesson_url']}''')
            bot.send_message(text=message_text, chat_id=tg_chat_id)
        timestamp = round(review['new_attempts'][0]['timestamp'])


if __name__ == '__main__':
    main()
