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
    delay = 3
    try:
        WebDriverWait(driver, delay).until(ec.presence_of_element_located((By.ID, 'header')))
        print("Page is ready.")
    except TimeoutException as e:
        return e


def get_bustabit_history(driver):
    table_class = "_2pVOOBSgMNp3OXBpclwWYS _2qBwQqUZR37-u5Hn1JqTpQ " \
                  "table table-sm table-striped table-bordered table-hover"
    rows = driver.find_elements_by_css_selector("table." + table_class)
    return rows


def get_table_from_csv():  # TODO: to be optimized (use the csv library properly...)
    # __location__ = os.path.realpath(
    #     os.path.join(os.getcwd(), os.path.dirname(__file__)))
    # try:
    #     file = open(os.path.join(__location__, 'BustaBit_multipler_history.csv'))
    # except FileNotFoundError as e:

    with open('persons.csv', 'rb') as f:
        full_history = csv.reader(f)
        table = list()
        bustabit_history_size = 25
        for row in full_history:
            table.append(row[1])
            if len(table) == bustabit_history_size:
                return table


def get_multiplier_value(driver):
    rows = get_bustabit_history(driver)
    csv_table = get_table_from_csv()
    for row in rows:
        value_hash = row.find_elements_by_tag_name("td")[4].text
        for csv_row in csv_table:
            if value_hash in csv_row[1]:
                pass
            else:
                value = row.find_elements_by_tag_name("td")[0].text
                print("Busted @:" + value)
                update_table(value, value_hash)
                print("csv file updated.")


def update_table(value, value_hash):  # TODO: to be optimized (use the csv library properly...)
    with open('BustaBit_multipler_history.csv',  'a+', newline='') as csv_file:
        file_writer = csv.writer(csv_file)
        file_writer.writerow([value, value_hash])


def close_driver(driver):
    try:
        driver.close()
    except TimeoutException as e:
        return e


def exit_handler(driver):
    close_driver(driver)
    print("driver close")
