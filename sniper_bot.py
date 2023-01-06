from time import sleep

from requests_html import HTMLSession, AsyncHTMLSession

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#session = HTMLSession()

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
    #check_appoitment(driver)
    #stock_checked = False
    #web_driver(url, stock_checked)




if __name__ == "__main__":
    main()

