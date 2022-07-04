import os
import random
import time

import numpy as np
import requests
import spintax
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager as GM

from credentials import password as passw
from credentials import username as usr


class Bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        self.bot = webdriver.Firefox(profile, executable_path=GM().install())
        self.bot.set_window_size(500, 950)
        with open(r'comments.txt', 'r') as f:
            coml = [line.strip().lower() for line in f]
        self.comments = coml
        self.url = "https://www.instagram.com/p/CPGo6pMLAAv/"

    def exit(self):
        bot = self.bot
        bot.quit()

    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(3)
        if check_exists_by_xpath(bot, "//button[text()='Aceptar todas']"):
            print("No cookies")
        else:
            bot.find_element_by_xpath("//button[text()='Aceptar todas']").click()
            print("Accepted cookies")

        time.sleep(5)
        bot.find_element_by_xpath('/html/body/div[1]/section/main/article/div/div/div/div[3]/button[1]').click()

        time.sleep(4)
        print("Logging in...")
        time.sleep(1)
        username_field = bot.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[3]/div/label/input')
        username_field.send_keys(self.username)

        find_pass_field = (
            By.XPATH, '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[4]/div/label/input')
        WebDriverWait(bot, 50).until(
            EC.presence_of_element_located(find_pass_field))
        pass_field = bot.find_element(*find_pass_field)
        WebDriverWait(bot, 50).until(
            EC.element_to_be_clickable(find_pass_field))
        pass_field.send_keys(self.password)
        bot.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]/button').click()
        time.sleep(4)

    def comment(self, comment):

        if self.url == None:
            print("No URL")
            return 0

        bot = self.bot
        url = self.url
        print('commenting...')
        bot.get(url)
        bot.implicitly_wait(1)

        bot.execute_script("window.scrollTo(0, window.scrollY + 300)")
        time.sleep(1)

        # bot.find_element_by_xpath(
        #     '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button').click()
        # time.sleep(2)

        bot.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[2]/button').click()

        # if check_exists_by_xpath(bot, '/html/body/div[1]/section/main/section/div'):
        #     print("skiped")
        #     return run.comment(random_comment())

        find_comment_box = (
            By.XPATH, '/html/body/div[1]/section/main/section/div[1]/form/textarea')
        WebDriverWait(bot, 50).until(
            EC.presence_of_element_located(find_comment_box))
        comment_box = bot.find_element(*find_comment_box)
        WebDriverWait(bot, 50).until(
            EC.element_to_be_clickable(find_comment_box))
        comment_box.click()
        time.sleep(1)
        comment_box.send_keys(comment)

        find_post_button = (
            By.XPATH, '/html/body/div[1]/section/main/section/div/form/button')
        WebDriverWait(bot, 50).until(
            EC.presence_of_element_located(find_post_button))
        post_button = bot.find_element(*find_post_button)
        WebDriverWait(bot, 50).until(
            EC.element_to_be_clickable(find_post_button))
        post_button.click()

        # edit this line to make bot faster
        time.sleep(2)
        # ---------------------------------



def random_comment():
    comment = random.choice(run.comments)
    return comment


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return True

    return False


run = Bot(usr, passw)
run.login()


count = 0
for comment in run.comments:
    if len(comment)>3:
        count +=1
        print(str(count)+comment)
        run.comment(comment)

print("Finished")
