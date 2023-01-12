import os
import pathlib
import pickle
import time
from getpass import getpass
from os.path import exists as file_exist
from time import sleep

import pyautogui
import PySimpleGUI as sg
import schedule
from pyautogui import screenshot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

  #type: ignorefrom pyautogui import screenshot

starting_web_browser = "Abriendo el navegador. POR FAVOR NO CERRAR hasta que se haya hecho el screenshot\n"
user_credentials = []

#layout for the UI
sg.theme('DarkAmber')

layout = [ [sg.Text("Sniper bot para prenotami."),],
           [sg.Multiline("STARTING",key= "-display-",auto_refresh= True, autoscroll= True, size=(55, 4), text_color="green", background_color="black")],
           [sg.Text("Usuario:     "), sg.InputText(key="-user_email-", text_color="black", background_color= "white")],
           [sg.Text("Contraseña:"), sg.InputText(password_char="*", key="-user_password-", text_color="black", background_color= "white")],
           [sg.Button("Empezar", key="-start-", button_color="green"), sg.Button("Cerrar", key="-stop-"),sg.Button("Ultimo Usuario", key="-l_user-"), sg.Button("Borrar Datos de Usuario", key="-Erase-", button_color="red")]
        ]


#check if there're no user_credentials
def create_user_credentials(user_credentials):
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

def web_driver_sign_in(url, u_email, u_password, driver):
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
        sleep(3)
        cittadinanza_per_discendenza = driver.find_element(By.XPATH, "//a[contains(@href, '/Services/Booking/224')]").click()
        sleep(3)
        no_appointment = None
        no_appointment = driver.find_element(By.XPATH, "//*[contains(text(),'Al momento non ci sono date disponibili per il servizio richiesto')]")
        try:
            return screenshot()
        except Exception:
            print("Algo salió mal o hay turno para el tramite. Seguro que algo salió mal.")  
    except Exception:
        print("Usuario o contraseña incorrectos")
        os.remove("user_credentials_file")

def main():
    window = sg.Window("Prenotami", layout)

    user_file = file_exist("user_credentials_file")

    #user is store in [0] and password is store in [1]
    user_credentials = []


    while True:
        
        event, values = window.read()

        if user_file == True:  
                

            user_credentials = read_user_credentials()
            
            #the user is the e-mail and is store here:
            u_email = user_credentials[0]
            u_password = user_credentials[1]
            
            window.Element("-user_email-").update(value=u_email)
            window.Element("-user_password-").update(value=u_password)

            window.refresh()
                      

        else:

            u_email = values["-user_email-"]
            u_password = values["-user_password-"]
            user_credentials.append(u_email)
            user_credentials.append(u_password)
            create_user_credentials(user_credentials)
        
             

        if event == sg.WIN_CLOSED or event == "-stop-":
            break
            exit()

        #check if exist user_credentials_file and if it doesn't ask for the credentials
        #the password is at least 8 characters and is store here:
            

        if event == "-start-":
            window.Element("-start-").update(disabled=True)
            window.Element("-user_email-").Update(disabled=True)
            window.Element("-user_password-").Update(disabled=True)

            print(starting_web_browser)

            url = "https://prenotami.esteri.it/"
            driver = webdriver.Firefox()

            web_driver_sign_in(url, u_email, u_password, driver)

            driver.close()
                


            
        """
        print(starting_web_browser)

        url = "https://prenotami.esteri.it/"

        
        driver = webdriver.Firefox()

        web_driver_sign_in(url, u_mail, u_password, driver)
        """

            
            
        
            

    window.close()  

        
    """
    else:
        window = sg.Window("Sniper Bot - Prnotami", layout2)
        
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or sg.Element("stop"):
                break

        window.close()
    """




    

        

    

if __name__ == "__main__":
    main()
    
    schedule.every(24).hours.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
    

