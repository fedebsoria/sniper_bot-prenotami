from time import sleep
import os
from requests_html import HTMLSession, AsyncHTMLSession
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pyautogui import screenshot
import pyautogui

import time

starting_web_browser = "Abriendo el navegador. POR FAVOR NO CERRAR hasta que se haya hecho el screenshot\n"

#takes screenshots

def screenshot():
    user = os.getlogin()
    daystr = time.strftime("%Y%m%d-%H%M%S")
    myScreenshot = pyautogui.screenshot()
    if os.name == "nt":
        user_screenshot_path = "c:/Users/{}/Desktop/{}.jpg".format(user, daystr)
        myScreenshot.save(user_screenshot_path)
        print("Screenshot guardado en {}".format(user_screenshot_path))
    else:
        user_screenshot_path_unix = "/home/{}/Desktop/{}.jpg".format(user, daystr)
        myScreenshot.save(user_screenshot_path_unix)
        print("Screenshot guardado en {}".format(user_screenshot_path_unix))
    
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
    sleep(3)
    cittadinanza_per_discendenza = driver.find_element(By.XPATH, "//a[contains(@href, '/Services/Booking/224')]").click()
    sleep(3)
    no_appointment = None
    no_appointment = driver.find_element(By.XPATH, "//*[contains(text(),'Al momento non ci sono date disponibili per il servizio richiesto')]")
    if no_appointment != None:
        return screenshot()
    else:
        print("Algo salió mal o hay turno para el tramite. Seguro que algo salió mal.")  


def main(): 
    #user input user and password
    u_mail = input("Ingrese el usuario: \n")  
    #martimicaela96@gmail.com
    u_password = getpass("Ingrese el password: \n") 
    #"Toby2903-"
    print(starting_web_browser)

    url = "https://prenotami.esteri.it/"

 
    driver = webdriver.Firefox()

    web_driver_sign_in(url, u_mail, u_password, driver)

    driver.close()

    

if __name__ == "__main__":
    main()

