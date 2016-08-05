# -*- coding -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from cookie_header.SeleniumCookieHeader import SeleniumCookieHeader


# http://www.loji.com/owner/login
# 17788353285
# 12345678


class SeleniumLuoji(SeleniumCookieHeader):

    def __init__(self):
        SeleniumCookieHeader.__init__(self)

    def open(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "headerUl"))
            )
        except Exception as e:
            print e
        else:
            self.get_cookie_header(driver)



luoji = SeleniumLuoji()
luoji.init("http://www.loji.com/owner/login")