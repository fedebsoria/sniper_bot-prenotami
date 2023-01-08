import os
import pathlib
import pickle
import time
from getpass import getpass
from time import sleep

import pyautogui
from pyautogui import screenshot
from requests_html import AsyncHTMLSession, HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from os.path import exists as file_exist

starting_web_browser = "Abriendo el navegador. POR FAVOR NO CERRAR hasta que se haya hecho el screenshot\n"
user_credentials = []


#check if there're no user_credentials
def get_user_credentials(user_credentials):
    if file_exist("user_credentials_file") != True:
        with open("user_credentials_file", "wb") as ud:
            pickle.dump(user_credentials, ud)
    else:
         pass

def read_user_credentials():
    with open("user_credentials_file", "rb") as uc:
        user_credentials = pickle.load(uc)
        return user_credentials


#takes screenshots

def screenshot():
    daystr = time.strftime("%Y%m%d-%H%M%S")
    myScreenshot = pyautogui.screenshot()
    user_screenshot_path = "{}/Desktop/{}.jpg".format(pathlib.Path.home(), daystr)
    myScreenshot.save(user_screenshot_path)
    print("Screenshot guardado en {}".format(user_screenshot_path))
    
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
        sleep(120)
    else:
        print("Algo salió mal o hay turno para el tramite. Seguro que algo salió mal.")  
 

def main(): 
    #user is store in [0] and password is store in [1]
    user_credentials = []

    if file_exist("user_credentials_file") != True:
        u_email = input("Ingrese el usuario:\n")
        u_password = getpass("Ingrese la contraseña:\n")
        user_credentials.append(u_email)
        user_credentials.append(u_password)
        pass
    else:
        print("Usuario y Contraseña ingresados")
        pass


    get_user_credentials(user_credentials)

    user_credentials = read_user_credentials()
    
    #user input user and password
    u_mail = user_credentials[0]  
    #martimicaela96@gmail.com
    u_password = user_credentials[1]
    #"Toby2903-"
    print(starting_web_browser)

    url = "https://prenotami.esteri.it/"

 
    driver = webdriver.Firefox()

    web_driver_sign_in(url, u_mail, u_password, driver)

    driver.close()

    

if __name__ == "__main__":
    main()

