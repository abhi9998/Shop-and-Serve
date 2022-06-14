# from fileinput import filename
# from asyncio.log import logger
from numpy import equal
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import unittest
import html_test_report

"""
Following POM design pattern for storing all web elements by pages

"""
# Page Elements
siteUrl = "http://localhost:3000/login"
adminSiteUrl = "http://localhost:3000/admin/login"
title = "ServeAndShop"
email = "//input[@id='Email']"
userEmailInput = "testuser5@test.com"
password = "//input[@id='password']"
passwordInput = "test@123"
submit = "//button[@class = 'btn btn-primary']"

# Page Functions
class loginPage(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())      
        self.driver.maximize_window()
        self.driver.get(siteUrl)
        print("Application Launched", self.driver.title)
        # logger.debug()
        # self.assertEqual(title, self.driver.title) 
        print("Application url is ", self.driver.current_url)
        # self.driver.quit()

    # Login as user
    def loginAsUser(self):
        self.driver.find_element(By.XPATH, email).click()
        self.driver.find_element(By.XPATH, email).clear()
        self.driver.find_element(By.XPATH, email).send_keys(userEmailInput)
        print("Email filled")
        self.driver.find_element(By.XPATH, password).click()
        self.driver.find_element(By.XPATH, password).clear()
        self.driver.find_element(By.XPATH, password).send_keys(passwordInput)
        print("Password filled")
        self.driver.find_element(By.XPATH,submit).click()
        print("Login successfully")

    def loginFailedAsUser(self):
        self.driver.find_element(By.XPATH, email).click()
        self.driver.find_element(By.XPATH, email).clear()
        self.driver.find_element(By.XPATH, email).send_keys(None)
        self.driver.find_element(By.XPATH, email).click()
        self.driver.find_element(By.XPATH, email).clear()
        self.driver.find_element(By.XPATH, email).send_keys(None)
        self.driver.find_element(By.XPATH,submit).click()

    def tearDown(self):
        self.driver.quit()  
    
    def setUpAdmin(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())      
        self.driver.maximize_window()
        self.driver.get(adminSiteUrl)
        print("Application Launched", self.driver.title)
        # self.assertEqual(title, self.driver.title) 
        print("Application url is ", self.driver.current_url)
        # self.driver.quit()
    
    def loginAsAdmin(self):
        self.driver.find_element(By.XPATH, email).click()
        self.driver.find_element(By.XPATH, email).clear()
        self.driver.find_element(By.XPATH, email).send_keys(userEmailInput)
        print("Email filled")
        self.driver.find_element(By.XPATH, password).click()
        self.driver.find_element(By.XPATH, password).clear()
        self.driver.find_element(By.XPATH, password).send_keys(passwordInput)
        print("Password filled")
        self.driver.find_element(By.XPATH,submit).click()
        print("Admin Login successfully")
   
    # Handle the Browser pop up
    def handleToastifyAlert(self):
        # self.driver.implicitly_wait(5)
        # self.driver.find_element(By.NAME, 'alert').click()
        self.popup = self.driver.switch_to.alert()
        assert "Logged in successfully" in self.popup.text
        self.popup.accept()
        # self.driver.window_handles
        print("Login alert switched")

    #  Assert the popup text 
    def assertPopupText(driver):
        loginText = "Logged In successfully"
        assert_equivalent(loginText, driver.switch_to.alert.text(), "Login alert incorrect")
        # print("Login Success")

    def switchWindow(self):
        self.driver.switch_to.new_window('tab')
        # self.driver.window_handles.
        # pass

    # Verify home page url for successfull login
    def verifyHomePage(self):
        # Assert for login validation
        self.homePageUrl = "http://localhost:3000/home"
        # assert self.homePageUrl in self.driver.current_url
        assert(self.homePageUrl, self.driver.current_url)
        
        # self.assert_equivalent(self.homePageUrl, self.driver.current_url)
        print ("HomePageVerified")

    def loginFailed(self):
        pass

    def tearDown(self):
        self.driver.quit()  

# if __name__ == '__main__':
#     unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner)
