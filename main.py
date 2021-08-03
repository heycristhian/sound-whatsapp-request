from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from loguru import logger
import time

DRIVER = webdriver.Chrome(executable_path="./driver/chromedriver.exe")


def process():
    DRIVER.get('https://web.whatsapp.com/')
    load_contact()
    send_message("*BOT STARTED SUCCESSFULLY*")
    send_message("*BOT FINISHED*")


def load_contact():
    while True:
        time.sleep(10)
        try:
            contact = 'sound-whatsapp-request'
            search_field = DRIVER.find_element_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
            search_field.click()
            search_field.send_keys(contact)
            search_field.send_keys(Keys.ENTER)
            return
        except NoSuchElementException:
            logger.error('Whatsapp needs to read QRCODE')


def send_message(message):
    message_field = DRIVER.find_elements_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
    message_field[1].click()
    time.sleep(3)
    message_field[1].send_keys(message)
    message_field[1].send_keys(Keys.ENTER)


if __name__ == '__main__':
    process()
