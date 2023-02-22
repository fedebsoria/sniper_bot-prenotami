import os
import sys
import pathlib
import pickle
import time
from getpass import getpass
from os.path import exists as file_exist
from time import sleep

import pyautogui
import PySimpleGUI as sg
from pyautogui import screenshot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

starting_web_browser = "Abriendo el navegador. POR FAVOR NO CERRAR hasta que se haya hecho el screenshot\n"

#layout for the UI
sg.theme('DarkAmber')

layout = [ [sg.Text("Sniper bot para prenotami."),],
           [sg.Multiline("Ingrese usuario y contraseña o use los ultimos datos guardados.\n",key= "-display-",auto_refresh= True, autoscroll= True, size=(55, 4), text_color="green", background_color="black")],
           [sg.Text("Usuario:     "), sg.InputText(key="-user_email-", text_color="black", background_color= "white")],
           [sg.Text("Contraseña:"), sg.InputText(password_char="*", key="-user_password-", text_color="black", background_color= "white")],
           [sg.Button("Empezar", key="-start-", button_color="green"), sg.Button("Cerrar", key="-stop-"),sg.Button("Ultimo Usuario", key="-l_user-"), sg.Button("Borrar Datos de Usuario", key="-Erase-", button_color="red")]
        ]


#check if there're no user_credentials and create it
def create_user_credentials_file(user_file):
    if not file_exist(user_file):
        with open(user_file, "wb") as ob:
            pickle.dump([], ob)
    else:
        pass

def write_user_credentials(user_credentials, user_file):
    if file_exist(user_file) != True:
        with open(user_file, "wb") as ud:
            pickle.dump(user_credentials, ud)
    else:
         pass

def read_user_credentials(user_file, user_credentials):
    try:
        with open(user_file, "rb") as uc:
            user_credentials = pickle.load(uc)
    except:
        pass
    return user_credentials


#takes screenshots

def screenshot_func(window):
    daystr = time.strftime("%Y%m%d-%H%M%S")
    myScreenshot = pyautogui.screenshot()
    user_screenshot_path = "{}/Desktop/{}.jpg".format(pathlib.Path.home(), daystr)
    myScreenshot.save(user_screenshot_path)
    window.Element("-display-").print("Screenshot guardado en {} \n Próxima captura en 24 hs.".format(user_screenshot_path))
    
    return myScreenshot

#enter the web and sign in

def web_driver_sign_in(url, u_email, u_password, driver, window):
    driver.get(url)
    sleep(3)
    email = driver.find_element("id", "login-email")
    password = driver.find_element("id", "login-password")
    email.send_keys(u_email)
    password.send_keys(u_password)
    password.send_keys(Keys.ENTER)
    sleep(3)
    #log_in_error = driver.find_element("id", "login-password-error")
    try:
        prenota = driver.find_element("id", "advanced").click()
        sleep(5)
        cittadinanza_per_discendenza = driver.find_element(By.XPATH, "//a[contains(@href, '/Services/Booking/224')]").click()
        sleep(5)
        no_appointment = None
        no_appointment = driver.find_element(By.XPATH, "//*[contains(text(),'Al momento non ci sono date disponibili per il servizio richiesto')]")
        try:
            screenshot_func(window)
        except Exception:
            window.Element("-display-").print("Algo salió mal o hay turno para el tramite.\n Seguro que algo salió mal.\n Cerrar y volver a correr.\n")  
    except Exception:
        window.Element("-display-").print("Usuario o contraseña incorrectos")
        window.Element("-start-").update(disabled=False)
        window.Element("-user_email-").Update(disabled=False)
        window.Element("-user_password-").Update(disabled=False)

def main():
    
    user_file = "user_credentials_file"
    user_file_path = "./user_credentials_file"
    #user is store in [0] and password is store in [1]
    user_credentials = []
    u_email = ""
    u_password = ""

    #create_user_credentials_file(user_file)
    
    
    user_credentials = read_user_credentials(user_file, user_credentials)
    if user_credentials != []:                        
            #the user is the e-mail and it is split here:
        u_email = user_credentials[0]
        u_password = user_credentials[1]
    else:
        write_user_credentials(user_credentials, user_file)



    window = sg.Window("Prenotami", layout)
    
    while True:
        #close the window and stop the script
        event, values = window.read()        
        if event == sg.WIN_CLOSED or event == "-stop-":
            sys.exit()            
  
        #erase the ./user_credentials_file.bin
        if event == "-Erase-":
            os.remove(user_file)
            window.Element("-display-").print("Datos de usuario borrados\n")
            pass
           
        #read the user_credentials_file in a list
        if event == "-l_user-":
            user_credentials = read_user_credentials(user_file, user_credentials)
            u_email = user_credentials[0]
            u_password = user_credentials[1]
            window.Element("-display-").print("Hay datos guardados\n")        
            window.Element("-user_email-").update(value=u_email)
            window.Element("-user_password-").update(value=u_password)
            window.Element("-display-").print("Datos obtenidos.\n")
            
        if event == "-start-":
                u_email = values["-user_email-"]
                u_password = values["-user_password-"]
                user_credentials.append(u_email)
                user_credentials.append(u_password)
                #stores new user's credentials in a binary
                write_user_credentials(user_credentials, user_file)
                window.Element("-start-").update(disabled=True)
                window.Element("-user_email-").Update(disabled=True)
                window.Element("-user_password-").Update(disabled=True)
                window.Element("-display-").print("Empezando...\n")

                window.Element("-display-").print(starting_web_browser)

                url = "https://prenotami.esteri.it/"
                driver = webdriver.Firefox()
                #starts browser an makes the screenshot
                web_driver_sign_in(url, u_email, u_password, driver, window)

                driver.close()

                #starts loop, every 24hs it will make an screenshot.
                while event != sg.WIN_CLOSED or event == "-stop-":
                    try:
                        #window.close()
                        sleep(10)
                        url = "https://prenotami.esteri.it/"
                        driver = webdriver.Firefox()

                        web_driver_sign_in(url, u_email, u_password, driver, window)

                        driver.close()
                    except Exception:
                        break



if __name__ == "__main__":
    main()
    


