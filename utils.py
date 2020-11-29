import os
import csv

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def get_driver():
    try:
        driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
    except TimeoutException as e:
        return "Can't find driver. Please make sure to have your " \
               "selenium server for Chrome up and running on the port 4444" + e
    return driver


def open_bustabit(driver, url):
    driver.get(url)
    delay = 1
    try:
        WebDriverWait(driver, delay).until(ec.presence_of_element_located((By.ID, 'header')))
        print("Page is ready.")
    except TimeoutException as e:
        return e


def get_table_from_csv():  # TODO: to be optimized (use the csv library properly...)
    # __location__ = os.path.realpath(
    #     os.path.join(os.getcwd(), os.path.dirname(__file__)))
    # try:
    #     file = open(os.path.join(__location__, 'BustaBit_multipler_history.csv'))
    # except FileNotFoundError as e:

    with open('BustaBit_multipler_history.csv', 'rb') as f:
        full_history = csv.reader(f)
        if len(list(full_history)) == 0:
            return []
        else:
            table = list()
            bustabit_history_size = 25
            for row in full_history:
                table.append(row[1])
                if len(table) == bustabit_history_size:
                    return table


def get_multiplier_value(driver):
    driver.find_elements_by_xpath('html/body/div/div/div/div[7]/div[1]/table/tbody/tr/td[1]')
    div = driver.find_element_by_class_name('switchable-area')
    breakpoint()
    rows = table.find_elements_by_tag_name('tr')
    csv_table = get_table_from_csv()
    for row in rows:
        value_hash = row.find_elements_by_tag_name("td")
        if len(csv_table) ==0:
                try:
                    update_table(value, value_hash)
                    print("csv file updated.")
                except Exception as e: # -*- coding: utf-8 -*-
                    print('Couldn''t File.')
        else:
            for csv_row in csv_table:
                if value_hash in csv_row[1]:
                    pass
                else:
                    value = row.find_elements_by_tag_name("td")[0].text
                    print("Busted @:" + value)
                    try:
                        update_table(value, value_hash)
                        print("csv file updated.")
                    except Exception as e: # -*- coding: utf-8 -*-
                        print('Couldn''t File.')


def update_table(value, value_hash):  # TODO: to be optimized (use the csv library properly...)
    with open('BustaBit_bust_history.csv',  'a+', newline='') as csv_file:
        file_writer = csv.writer(csv_file)
        if value_hash is not None:
            file_writer.writerow([value, value_hash])


def close_driver(driver):
    try:
        driver.close()
    except TimeoutException as e:
        return e

def get_previous_games_data(driver, starting_game_number, finishing_game_number):
    game_numbers = list(range(starting_game_number, finishing_game_number))
    for game_number in game_numbers:
        url = "https://www.bustabit.com/game/" + str(game_number)
        open_bustabit(driver, url)
        print(str(game_number))
        p_tag = driver.find_elements_by_class_name('_2IumaQfnOQsiJTuwTJZlvp')
        bust = p_tag[0].text.split()[2].split('x')[0]
        print('busted @ ' + bust)
        update_table(bust, game_number)
        print("csv file updated")


def exit_handler(driver):
    close_driver(driver)
    print("Driver closed")
