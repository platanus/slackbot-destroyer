#!/usr/bin/python
# -*- coding: utf-8 -*-
from slack import WebClient
from slack import RTMClient
from constants import *
import logging


@RTMClient.run_on(event='message')
def handle_message(**payload):
    message_data = payload['data']
    if message_data.get('subtype') is None and 'text' in message_data:
        handle_user_message(message_data)
    if message_data.get('subtype') == 'bot_message':
        handle_bot_message(message_data)


def handle_user_message(message_data):
    pass


def handle_bot_message(message_data):
    logging.debug(f"Bot message from: {message_data.get('user')} in channel: {message_data.get('channel')}.")
    if message_data.get('user') == 'USLACKBOT':
        logging.info(f"Deleting slackbot message: {message_data.get('text')}.")
        delete_message(message_data.get('channel'), message_data.get('ts'))


def delete_message(channel, timestamp):
    response = WebClient(SLACK_USER_TOKEN).chat_delete(channel=channel, ts=timestamp, as_user=True)
    if response.get('ok'):
        logging.info(f"Message deleted successfully.")
    else:
        logging.error(f"Error deleting message: {response.get('error')}.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    rtm_client = RTMClient(token=SLACK_BOT_TOKEN)
    rtm_client.start()
