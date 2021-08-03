from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from loguru import logger
import time
from datetime import datetime
import re
import urllib.parse

DRIVER_WHATSAPP = webdriver.Chrome(executable_path="./driver/chromedriver.exe")
DRIVER_YOUTUBE = webdriver.Chrome(executable_path="./driver/chromedriver.exe")
songs = []


def play_music(music):
    songs.append(music)
    encode_search = urllib.parse.quote(music)
    DRIVER_YOUTUBE.get(f"https://www.youtube.com/results?search_query={encode_search}")
    DRIVER_YOUTUBE.find_element_by_xpath('//*[@id="img"]').click()
    songs.remove(music)


def read_text():
    date = change_time()
    message = f"*BOT STARTED SUCCESSFULLY {date}*"
    send_message(message)
    logger.info(message)
    regex = r"\!music(.*)$"
    checker = True

    while checker:
        try:
            text = DRIVER_WHATSAPP.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[2]').text
        except Exception as err:
            logger.error(err)
            text = DRIVER_WHATSAPP.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]').text

        index = text.index(date) if text else 0
        text = text[index:]
        matches = re.finditer(regex, text, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            music = match.group()[6:].strip()
            date = change_time()
            if music not in songs:
                play_music(music)
                message = f"Music successfully added {date}: *{music}*"
                send_message(message)
                logger.info(message)
            else:
                message = f"Music is already in the queue {date}: *{music}*"
                send_message(message)
                logger.warning(message)
        time.sleep(2)
    send_message("*BOT FINISHED*")


def process():
    DRIVER_WHATSAPP.get('https://web.whatsapp.com/')
    load_contact()
    read_text()


def load_contact():
    while True:
        time.sleep(10)
        try:
            contact = 'sound-whatsapp-request'
            search_field = DRIVER_WHATSAPP.find_element_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
            search_field.click()
            search_field.send_keys(contact)
            search_field.send_keys(Keys.ENTER)
            return
        except NoSuchElementException:
            logger.error('Whatsapp needs to read QRCODE')


def send_message(message):
    message_field = DRIVER_WHATSAPP.find_elements_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
    message_field[1].click()
    time.sleep(3)
    message_field[1].send_keys(message)
    message_field[1].send_keys(Keys.ENTER)


def change_time():
    return str(datetime.now().time())


if __name__ == '__main__':
    process()
