import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

def exceptionFalse(driver):
    exception = False
    print('Заявка бітті. Барып демал')
    driver.quit()
    sys.exit(1)

def launchBrowser():
    driver = webdriver.Chrome('C:/Users/techsupport/AppData/Local/Programs/Python/Python311/chromedriver')
    driver.maximize_window() # For maximizing window
    driver.implicitly_wait(10) # gives an implicit wait for 20 seconds

    driver.get('https://support.demeu.com/')

    error_message = True

    while(error_message==True):
        try:
            surname_name = input("Введи свою Фамилию и Имя, например вот так: Соловьев Даниил \n")
        except ValueError:
            print('Неправильный ввод')
            error_message = True

        try:
            j_username = input("Логин ")
        except ValueError:
            print('Неправильный ввод')
            error_message = True
        username = driver.find_element(By.NAME, 'j_username')
        username.send_keys(j_username, Keys.TAB)

        try:
            j_password = input("Пароль ")
        except ValueError:
            print('Неправильный ввод')
            error_message = True
        password  = driver.find_element(By.NAME, "j_password")
        password.send_keys(j_password + Keys.ENTER+Keys.ENTER)

        if("Ошибка в имени пользователя или пароле" in driver.page_source):
            error_message = True
            print('Неверный логин или пароль. Давай по новой')
        else:
            error_message = False


        driver.get('https://support.demeu.com/')


    try:
        elem = driver.find_element(By.XPATH, '//*[@id="ReqSummary"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/a/b')
        elem.click()  # заявки в очереди
    except NoSuchElementException:
        print('Заявка бітті. Барып демал')
        driver.quit()
        sys.exit(1)

    exception = True
    while(exception == True):
        try:
            strings = driver.find_elements(By.ID, "tooltip")  # открываем первую заявку
            string = strings[0]
            string.click()
        except StaleElementReferenceException:
            exceptionFalse(driver)
        except NoSuchElementException:
            exceptionFalse(driver)
        except IndexError:
            exceptionFalse(driver)

        elem = driver.find_element(By.ID, "span_resolutionDetails")  # решение открываем
        elem.click()

        button = driver.find_element(By.XPATH,
        '//*[@id="resolutionDetails"]/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/input')
        button.click()  # галочку ставим

        userID = driver.find_element(By.NAME, "technicianID")
        userID.click()
        userID = driver.find_element(By.XPATH, '//*[@id="0.0#'+ surname_name + '"]')
        userID.click()

        requestType = driver.find_element(By.NAME, "requestType")
        requestType.click()
        requestType = driver.find_element(By.XPATH, '//*[@id="TypeListNew"]/table/tbody/tr/td[1]/select/option[4]')
        requestType.click()

        workMinutes = driver.find_element(By.NAME,'workMinutes')
        #4
        workMinutes.send_keys(Keys.ARROW_RIGHT + Keys.BACKSPACE)
        workMinutes.send_keys('10', Keys.TAB)

        description = driver.find_element(By.NAME, 'description')
        description.send_keys('Выполнено. Функционирует')

        save = driver.find_element(By.NAME,'saveAndCloseReqButton')
        save.click()







launchBrowser()




