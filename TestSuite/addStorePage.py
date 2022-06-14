from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import unittest

"""
Following POM design pattern for storing all web elements by pages

"""
# Page Elements
siteUrl = "http://localhost:3001/admin/addstore"
storeName = "//*[@id='name']"
storeAddress = "//*[@id='address']"
storeCity = "//input[@id='city']"
storePincode = "//input[@id='pincode']"

# Page Functions
class addStorePage(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())      
        self.driver.maximize_window()
        self.driver.get(siteUrl)
        print("Application Launched", self.driver.title)
        # self.assertEqual(title, self.driver.title) 
        print("application url is ", self.driver.current_url)
        # self.driver.quit()
    
    def addStore(self):
        self.driver.find_element(By.XPATH, storeName).click()
        self.driver.find_element(By.XPATH, storeName).clear()
        self.driver.find_element(By.XPATH, storeName).send_keys("Hasty Market")
        self.driver.find_element(By.XPATH, storeAddress).click()
        self.driver.find_element(By.XPATH, storeAddress).clear()
        self.driver.find_element(By.XPATH, storeAddress).send_keys("GlassGow")
        self.driver.find_element(By.XPATH, storeCity).click()
        self.driver.find_element(By.XPATH, storeCity).clear()
        self.driver.find_element(By.XPATH, storeCity).send_keys("Kitchener")
        self.driver.find_element(By.XPATH, storePincode).click()
        self.driver.find_element(By.XPATH, storePincode).clear()
        self.driver.find_element(By.XPATH, storePincode).send_keys("Kitchener")
        self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()

    def tearDown(self):
        self.driver.quit()  


