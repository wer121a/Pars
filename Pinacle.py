import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
import os
from threading import Thread
from multiprocessing import Process, Queue


base = pd.DataFrame(columns=["Name", "p1", "x", 'p2', 'f1', 'f2', 'totm', 'totb']) # Создание базового df


def fast (url): # Старт браузера

    global driver # Передача драйвера в общий доступ

    option = webdriver.ChromeOptions() # Создание функций к driver
    option.add_argument('User-Agent=Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)') # Шапка
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument('--ignore-certificate-errors') # Игнорируем ошибку Certificate
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\Сергей\Desktop\Python\Progect\Selenium(test)\chromedriver_win32\chromedriver.exe',
        options=option) # Драйвер настройка и путь до webdriver
    
    driver.maximize_window() # Режим окна во весь экран
    sleep(2)
    driver.get(url=url) # переход по ссылки принятой функцией
    sleep(4)
    driver.find_element(By.XPATH, '//p[@style="margin: 10px 0;"]').click()
    sleep(4)
    


def pin_futball(travel): # Парс футбольных событий(Идентичны для тениса, баскетбола)
    global base_olimp

    fast('https://pin-1500.xyz/') # Запуск функции с передачей параметра

    while True:
        if driver.find_element(By.XPATH, "//h3[@class='style_desktop_heading__I3fIu']"):
            break
        else:
            sleep(2)
    
    driver.find_element(By.XPATH, "//i[@class='icon-chevron-right-sml style_icon__1cJAy']").click()
    sleep(5)

