import os
import sys
import pathlib
import pickle
import time
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
           [sg.Button("Empezar", key="-start-", button_color="green"), sg.Button("Cerrar", key="-stop-"),sg.Button("Ultimo Usuario", key="-l_user-"), sg.Button("Borrar Datos de Usuario", key="-erase-", button_color="red")]
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

def web_driver_sign_in( u_email, u_password, window):
    url = "https://prenotami.esteri.it/"
    driver = webdriver.Firefox()
    shoot_success = False
    driver.get(url)
    sleep(3)
    email = driver.find_element("id", "login-email")
    password = driver.find_element("id", "login-password")
    email.send_keys(u_email)
    password.send_keys(u_password)
    password.send_keys(Keys.ENTER)
    sleep(10)
    try:
        prenota = driver.find_element("id", "advanced").click()
        sleep(10)
        cittadinanza_per_discendenza = driver.find_element(By.XPATH, "//a[contains(@href, '/Services/Booking/224')]").click()
        sleep(10)
        no_appointment = None
        no_appointment = driver.find_element(By.XPATH, "//*[contains(text(),'Al momento non ci sono date disponibili per il servizio richiesto')]")
        try:
            #in here starts the screenshot
            screenshot_func(window)
            shoot_success = True
            driver.close()
        except Exception:
            window.Element("-display-").print("Algo salió mal o hay turno para el tramite.\n Seguro que algo salió mal.\n Cerrar y volver a correr.\n")  
    except Exception:
        window.Element("-display-").print("Usuario o contraseña incorrectos")
        window.Element("-start-").update(disabled=False)
        window.Element("-user_email-").Update(disabled=False)
        window.Element("-user_password-").Update(disabled=False)
    
    return shoot_success

#changes the buttons so they can't be used by the user. If not it'll only starts the daily loop
def change_buttons_disabled(window, element_key):
    window.Element(element_key).Update(disabled=True, button_color="black")
    window.refresh()

#writes in the display a message
def display_refresh(window, text):
    window.Element("-display-").print(text)
    window.refresh


def main():
    
    shoot_success = False
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
        event, values = window.read() #type: ignore        
        if event in (sg.WIN_CLOSED, "-stop-"):
            sys.exit()            
  
        #erase the ./user_credentials_file.bin
        if event in ("-Erase-"):
            os.remove(user_file)
            display_refresh(window, "Datos de usuario borrados\n")
            pass
           
        #read the user_credentials_file in a list
        if event in ("-l_user-"):
            user_credentials = read_user_credentials(user_file, user_credentials)
            u_email = user_credentials[0]
            u_password = user_credentials[1]
            display_refresh(window, "Hay datos guardados\n")      
            window.Element("-user_email-").update(value=u_email)
            window.Element("-user_password-").update(value=u_password)
            display_refresh(window, "Datos obtenidos.\n")
            
        if event in ("-start-"):
            u_email = values["-user_email-"]
            u_password = values["-user_password-"]
            user_credentials.append(u_email)
            user_credentials.append(u_password)
            #stores new user's credentials in a binary
            write_user_credentials(user_credentials, user_file)
            #disable the numbers
            change_buttons_disabled(window, "-stop-")
            change_buttons_disabled(window, "-l_user-")
            change_buttons_disabled(window, "-erase-")
            display_refresh(window, "Empezando...\n")
            display_refresh(window, starting_web_browser)
            #starts browser an makes the screenshot
            shoot_success = web_driver_sign_in(u_email, u_password, window)
            window.refresh()

        #starts loop, every 24hs it will make an screenshot.
                
        while shoot_success == True:
            window.Read(timeout=(((1000*60)*60)*24)) #this gives 24 hours
            #makes a click in start
            window.write_event_value("-start-", any)
            window.refresh()

            if event in ("-start-"):
                web_driver_sign_in(u_email, u_password, window)
                window.Read(timeout=(1000))
                window.refresh()
            else:
                break
            #test


if __name__ == "__main__":
    main()
    


