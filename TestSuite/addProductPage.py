from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

"""
Following POM design pattern for storing all web elements by pages

"""
# Page Elements
siteUrl = "http://localhost:3001/admin/addstore"
data = ""


# Page Functions
class addProductPage():
    
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())      
        self.driver.maximize_window()
        self.driver.get(siteUrl)
        print("Application Launched", self.driver.title)
        # self.assertEqual(title, self.driver.title) 
        print("application url is ", self.driver.current_url)
        # self.driver.quit()
    
    def addProduct(self):
        pass
        # TODO
        # Handle alert


    def tearDown(self):
        self.driver.quit()  

     

