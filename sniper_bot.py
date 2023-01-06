from time import sleep

from requests_html import HTMLSession, AsyncHTMLSession

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pyautogui

import time


#session = HTMLSession()

#takes screenshots

def screenshot():
    daystr = time.strftime("%Y%m%d-%H%M%S")
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r"/home/fede/Desktop/{}.jpg".format(daystr))
    return myScreenshot

#enter the web and sign in

def web_driver_sign_in(url, u_mail, u_password, driver):
    
    driver.get(url)
    sleep(3)
    email = driver.find_element("id", "login-email")
    password = driver.find_element("id", "login-password")

    email.send_keys(u_mail)
    password.send_keys(u_password)
    password.send_keys(Keys.ENTER)
    sleep(3)
    prenota = driver.find_element("id", "advanced").click()
    sleep(5)
    cittadinanza_per_discendenza = driver.find_element(By.XPATH, "//a[contains(@href, '/Services/Booking/224')]").click()
    sleep(5)
    no_appointment = None
    no_appointment = driver.find_element(By.XPATH, "//*[contains(text(),'Al momento non ci sono date disponibili per il servizio richiesto')]")
    if no_appointment != None:
        return screenshot()  


    """def check_stock(url):

    while True:
        stock_checked = False
        session = HTMLSession()
        r = session.get(url)
        buy_zone = r.html.find("#buy-now-button")
        if len(buy_zone) > 0:
            print("Hay stock.")
            stock_checked = True
            #return stock_checked
            #pass
            web_driver(url, stock_checked)
        else:
            print("No hay stock.")
        sleep(30)
        return stock_checked
"""


def main():    

    url = "https://prenotami.esteri.it/"

    u_mail = "martimicaela96@gmail.com"
    u_password = "Toby2903-"

    driver = webdriver.Firefox()

    web_driver_sign_in(url, u_mail, u_password, driver)

    




if __name__ == "__main__":
    main()

