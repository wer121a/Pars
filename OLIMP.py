#Импорт библиотек
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
    
    # while True: # Цикл для проверки условия, пока оно не выполнится

        # if driver.find_element(By.XPATH, ".//button[@data-qa='authorizedButton']"): # Условие для нажатия кнопки "Вход", пока она не прогрузится в браузере
            # driver.find_element(By.XPATH, ".//button[@data-qa='authorizedButton']").click() # Нажатие на "Вход"
            # sleep(1)
            # driver.find_element(By.XPATH, "//input[@class='input--bQg0a']").send_keys('89156196802') # Ввод логина
            # sleep(1)
            # driver.find_element(By.XPATH, "//input[@class='input--bQg0a password--GQKrc']").send_keys('Qp60N111') # Ввод пароля
            # sleep(1)
            # driver.find_element(By.XPATH, "//button[@type='submit']").click() # Нажатие кнопки "авторизоваться"
            # sleep(1)
            # break

    while True: # Цикл для проверки условия, пока оно не выполнится

        if driver.find_element(By.CLASS_NAME, 'menuItem--qbMBY'): # Условие для переходу к "Лайв"
            driver.find_element(By.CLASS_NAME, 'menuItem--qbMBY').click() # Переход в лайв
            break
   
    sleep(2)


def futball(travel): # Парс футбольных событий(Идентичны для тениса, баскетбола)

    global base_olimp

    fast('https://www.olimp.bet') # Запуск функции с передачей параметра

    source_futbal = driver.find_elements(By.CLASS_NAME, 'root--kGzgY') # Тип игры идентичнцы, собираем их все
    pp = source_futbal[0] # Футбол стоит в списке первым, обращение к нему, в дальнейшем обращения для тениса и баскетбола будут последовательные

    while True:

        sleep(3)
    
        base_olimp = base.copy() # Копирование конструкции df (Каждый цикл будет пустой df)
      
        if pp.find_elements(By.CLASS_NAME, 'content--V86vO'): # Условие, если есть событие, продолжаем парсить, если нет, цикл будет запускаться заново, пока не появится событие
            conteiner_futball = pp.find_elements(By.CLASS_NAME, 'content--V86vO') # Собираем все события по футболу
            lis = [] # Создания листа для кэф.

            for sob_futbal in conteiner_futball: # Обращаемся к каждому событию
                name_futball = sob_futbal.find_element(By.CLASS_NAME, 'name--R2XME').text.replace('\n','') # Собираем название команд и удаляем лишние символы "\n"
                coef_futball = sob_futbal.find_elements(By.XPATH, ".//button[@data-qa='betButton']") # Собираем все коэффициенты
            
                for y in coef_futball: # Перебираем каждый коэффициент
                    lis.append(y.text) # Добавляем каждый кэф. в список
                    
                pars = {"Name":name_futball, "p1":lis[0], "x":lis[1], 'p2':lis[2], 'f1':lis[3], 'f2':lis[4], 'totm':lis[5], 'totb':lis[6]} # Формируем строчку df с собранными данными
                base_olimp = pd.concat([base_olimp, pd.DataFrame([pars])], ignore_index=True) # Добавляем сформированную строчку в base_olimp
                del lis[0:7] # Чистим список
        
            travel.put(base_olimp.copy()) # Передаём сформированный df с коэф. в Queue (добавляем в очередь, из которой он будет взят в файле processing)


def tennis(travel): # Парс тенисных событий

    global base_olimp

    fast('https://www.olimp.bet')

    suorce_futbal = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    pp = suorce_futbal[0] # Футбол
    sleep(2)
    pp.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE isOpen"]').click() # Закрываем футбол
    sleep(2)

    
    source_tennis = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    p = source_tennis[1] # Тенис 
    sleep(2)
    p.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE"]').click() # Нажимаем на тенис, чтобы открылись события (далее идентично)
    sleep(2)

    while True:
        sleep(3)
        base_olimp = base.copy()
        
        if p.find_elements(By.CLASS_NAME, 'content--V86vO'):
            conteiner_tennis = p.find_elements(By.CLASS_NAME, 'content--V86vO')
            lis = []

            for sob_tennis in conteiner_tennis:
                name_tennis = sob_tennis.find_element(By.CLASS_NAME, 'name--R2XME').text.replace('\n','')
                coef_tennis = sob_tennis.find_elements(By.XPATH, ".//button[@data-qa='betButton']")
                    
                for y in coef_tennis:
                    lis.append(y.text)    
                    
                pars = {"Name":name_tennis, "p1":lis[0], "x":lis[1], 'p2':lis[2], 'f1':lis[3], 'f2':lis[4], 'totm':lis[5], 'totb':lis[6]}
                base_olimp = pd.concat([base_olimp, pd.DataFrame([pars])], ignore_index=True)
                del lis[0:7]

            travel.put(base_olimp.copy())


def bascet(travel): # Идентично тенису

    global base_olimp

    fast('https://www.olimp.bet')

    suorce_futbal = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    pp = suorce_futbal[0]
    sleep(2)
    pp.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE isOpen"]').click()
    sleep(2)
    
    source_bascet = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    p = source_bascet[2]
    sleep(2)
    p.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE"]').click()
    sleep(2)

    while True:   
        base_olimp = base.copy()
        
        if p.find_element(By.CLASS_NAME, 'content--V86vO'):
            conteiner_bascet = p.find_elements(By.CLASS_NAME, 'content--V86vO')
            lis = []

            for sob_bascet in conteiner_bascet:
                name_bascet = sob_bascet.find_element(By.CLASS_NAME, 'name--R2XME').text.replace('\n','')
                coef_tennis = sob_bascet.find_elements(By.XPATH, ".//button[@data-qa='betButton']")
                    
                for y in coef_tennis:
                    lis.append(y.text)    

                pars = {"Name":name_bascet, "p1":lis[0], "x":lis[1], 'p2':lis[2], 'f1':lis[3], 'f2':lis[4], 'totm':lis[5], 'totb':lis[6]}
                base_olimp = pd.concat([base_olimp, pd.DataFrame([pars])], ignore_index=True)
                del lis[0:7]

        travel.put(base_olimp.copy())


def ft(travel): # Идентично, только теннис открываем, футбол уже открыт при загрузки страницы
    global base_olimp

    fast('https://www.olimp.bet')

    source_tennis = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    p = source_tennis[1]
    sleep(2)
    p.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE"]').click()
    sleep(2)


    while True:
        base_olimp = base.copy()
        
        if driver.find_element(By.CLASS_NAME, 'content--V86vO'):
            conteiner_bascet = driver.find_elements(By.CLASS_NAME, 'content--V86vO')
            lis = []

            for sob_bascet in conteiner_bascet:
                name_bascet = sob_bascet.find_element(By.CLASS_NAME, 'name--R2XME').text.replace('\n','')
                coef_tennis = sob_bascet.find_elements(By.XPATH, ".//button[@data-qa='betButton']")
                        
                for y in coef_tennis:
                    lis.append(y.text)    

                pars = {"Name":name_bascet, "p1":lis[0], "x":lis[1], 'p2':lis[2], 'f1':lis[3], 'f2':lis[4], 'totm':lis[5], 'totb':lis[6]}
                base_olimp = pd.concat([base_olimp, pd.DataFrame([pars])], ignore_index=True)
                del lis[0:7]
            
            travel.put(base_olimp.copy())

def fb(travel): # Идентично, только баскетбол открываем, футбол уже открыт при загрузки страницы

    global base_olimp

    fast('https://www.olimp.bet')

    source_bascet = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    ppp = source_bascet[2]
    sleep(2)
    ppp.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE"]').click()
    sleep(2)


    while True:
        base_olimp = base.copy()
        
        if driver.find_element(By.CLASS_NAME, 'content--V86vO'):
            conteiner_bascet = driver.find_elements(By.CLASS_NAME, 'content--V86vO')
            lis = []

            for sob_bascet in conteiner_bascet:
                name_bascet = sob_bascet.find_element(By.CLASS_NAME, 'name--R2XME').text.replace('\n','')
                coef_tennis = sob_bascet.find_elements(By.XPATH, ".//button[@data-qa='betButton']")
                        
                for y in coef_tennis:
                    lis.append(y.text)    
                    
                pars = {"Name":name_bascet, "p1":lis[0], "x":lis[1], 'p2':lis[2], 'f1':lis[3], 'f2':lis[4], 'totm':lis[5], 'totb':lis[6]}
                base_olimp = pd.concat([base_olimp, pd.DataFrame([pars])], ignore_index=True)
                del lis[0:7]

            travel.put(base_olimp.copy())

def bt(travel): #Идентично, только футбол закрываем и открываем теннис и баскетбол
    
    global base_olimp

    fast('https://www.olimp.bet')

    suorce_futbal = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    pp = suorce_futbal[0]
    sleep(2)
    pp.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE isOpen"]').click()
    sleep(2)
    source_tennis = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    p = source_tennis[1]
    sleep(2)
    p.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE"]').click()
    sleep(2)
    source_bascet = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    ppp = source_bascet[2]
    sleep(2)
    ppp.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE"]').click()
    sleep(2)

    while True:
        sleep(2)        
        base_olimp = base.copy()
        
        if driver.find_element(By.CLASS_NAME, 'content--V86vO'):
            conteiner_bascet = driver.find_elements(By.CLASS_NAME, 'content--V86vO')
            lis = []

            for sob_bascet in conteiner_bascet:
                name_bascet = sob_bascet.find_element(By.CLASS_NAME, 'name--R2XME').text.replace('\n','')
                coef_tennis = sob_bascet.find_elements(By.XPATH, ".//button[@data-qa='betButton']")
                
                for y in coef_tennis:
                    lis.append(y.text)    
                
                pars = {"Name":name_bascet, "p1":lis[0], "x":lis[1], 'p2':lis[2], 'f1':lis[3], 'f2':lis[4], 'totm':lis[5], 'totb':lis[6]}
                base_olimp = pd.concat([base_olimp, pd.DataFrame([pars])], ignore_index=True)
                del lis[0:7]
                
            travel.put(base_olimp.copy())

def fbt(travel): #Идентично

    global base_olimp

    fast('https://www.olimp.bet')

    source_tennis = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    p = source_tennis[1]
    sleep(2)
    p.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE"]').click()
    sleep(2)
    source_bascet = driver.find_elements(By.CLASS_NAME, 'root--kGzgY')
    ppp = source_bascet[2]
    sleep(2)
    ppp.find_element(By.XPATH, './/span[@class="iconArrow--bwAeE"]').click()
    sleep(2)

    while True:
        sleep(2)        
        base_olimp = base.copy()
        
        if driver.find_element(By.CLASS_NAME, 'content--V86vO'):
            conteiner_bascet = driver.find_elements(By.CLASS_NAME, 'content--V86vO')
            lis = []

            for sob_bascet in conteiner_bascet:
                name_bascet = sob_bascet.find_element(By.CLASS_NAME, 'name--R2XME').text.replace('\n','')
                coef_tennis = sob_bascet.find_elements(By.XPATH, ".//button[@data-qa='betButton']")
                
                for y in coef_tennis:
                    lis.append(y.text)    
                
                pars = {"Name":name_bascet, "p1":lis[0], "x":lis[1], 'p2':lis[2], 'f1':lis[3], 'f2':lis[4], 'totm':lis[5], 'totb':lis[6]}
                base_olimp = pd.concat([base_olimp, pd.DataFrame([pars])], ignore_index=True)
                del lis[0:7]
                
            travel.put(base_olimp.copy())