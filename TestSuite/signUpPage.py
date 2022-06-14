from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import unittest


"""
Following POM design pattern for storing all web elements by pages

"""
# Page Elements
siteUrl = "http://localhost:3000/signup"
title = "ServeAndShop"
name = "//input[@id='name']"
address = "//input[@id='address']"
city = "//input[@id='city']"
pincode = "//input[@id='pincode']"
email = "//input[@id='email']"
contactno = "//input[@id='contactNo']"
password = "//input[@id='password']"
rePassword = "//input[@id='rePassword']"

# Page Functions
class signUpPage(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())      
        self.driver.maximize_window()
        self.driver.get(siteUrl)
        print("Application Launched", self.driver.title)
        # self.assertEqual(title, self.driver.title) 
        print("application url is ", self.driver.current_url)
        # self.driver.quit()
    
    def userSignUp(self):
        self.driver.find_element(By.XPATH, name).click()
        self.driver.find_element(By.XPATH, name).clear()
        self.driver.find_element(By.XPATH, name).send_keys("MeenaAutomation")
        self.driver.find_element(By.XPATH, address).click()
        self.driver.find_element(By.XPATH, address).clear()
        self.driver.find_element(By.XPATH, address).send_keys("TestAddress")
        self.driver.find_element(By.XPATH, city).click()
        self.driver.find_element(By.XPATH, city).clear()
        self.driver.find_element(By.XPATH, city).send_keys("TestCity")
        self.driver.find_element(By.XPATH, pincode).click()
        self.driver.find_element(By.XPATH, pincode).clear()
        self.driver.find_element(By.XPATH, pincode).send_keys("N2M 5H3")
        self.driver.find_element(By.XPATH, email).click()
        self.driver.find_element(By.XPATH, email).clear()
        self.driver.find_element(By.XPATH, email).send_keys("snsuser@gmail.com")
        self.driver.find_element(By.XPATH, contactno).click()
        self.driver.find_element(By.XPATH, contactno).clear()
        self.driver.find_element(By.XPATH, contactno).send_keys("8090080809")
        self.driver.find_element(By.XPATH, password).click()
        self.driver.find_element(By.XPATH, password).clear()
        self.driver.find_element(By.XPATH, password).send_keys("testuser")
        self.driver.find_element(By.XPATH, rePassword).click()
        self.driver.find_element(By.XPATH, rePassword).clear()
        self.driver.find_element(By.XPATH, rePassword).send_keys("testuser")
        self.driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
        print("UserSignUp passed")

    def signOutUser(self):
        self.driver.find_element(By.XPATH, "//a[@href='/signout'] ").click()
    
        
    def verifyUser(self):
        # Assert for user validation
        pass

    def tearDown(self):
        self.driver.quit()  
