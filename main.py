import requests
import os
import telegram
import logging

from dotenv import load_dotenv
from textwrap import dedent
from time import sleep


USER_REVIEWS_LONG_POLLING = 'https://dvmn.org/api/long_polling/'


class TelegramHandler(logging.Handler):
    def __init__(self, tg_bot, tg_chat_id):
        super().__init__()
        self.tg_chat_id = tg_chat_id
        self.handler_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.handler_bot.send_message(text=log_entry, chat_id=self.tg_chat_id)


def main():
    load_dotenv('.env')
    dvmn_token = os.environ['DVMN_TOKEN']
    tg_token = os.environ['TG_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=tg_token)
    headers = {'Authorization': 'Token {0}'.format(dvmn_token)}
    timestamp = None
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramHandler(bot, tg_chat_id))
    logger.info('Bot started')
    while True:
        try:
            response = requests.get(USER_REVIEWS_LONG_POLLING, headers=headers, timeout=90, params={'Timestamp': timestamp})
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            logger.debug('Read timeout on request')
            continue
        except ConnectionError:
            logger.warning('Connection error on request')
            sleep(30)
            continue
        review = response.json()
        if review['status'] == 'found':
            if review['new_attempts'][0]['is_negative']:
                last_review = review['new_attempts'][0]
                timestamp = last_review['timestamp']
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
            logger.info('Bot has processed review')

        else:
            continue


if __name__ == '__main__':
    main()
