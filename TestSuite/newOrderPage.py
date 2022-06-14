from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import loginPage
"""
Following POM design pattern for storing all web elements by pages

"""
# Page Elements
siteUrl = "http://localhost:3001/admin/addstore"
newOrderNavBar = "//div[@class='navbar-nav']/a[text()='NewOrder']"
newOrderUrl = "http://localhost:3000/neworder/stores"
search = "//div[@class='sc-papXJ bthVWF']/div"
siteUrl = "http://localhost:3000/login"
storeSelection = "//*[@id='search']"
storename = '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div/button'


# Page Functions
class newOrder(unittest.TestCase):
    def setUpNewOrder(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())      
        self.driver.maximize_window()
        self.driver.get(siteUrl)
        self.driver.get(newOrderUrl)
    
    def newOrderNewTab(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(newOrderUrl)
    
    def wait(self):
        self.driver.implicitly_wait(10)

    def selectStore(self):
        self.driver.find_element(By.XPATH, storeSelection).click()
        self.driver.find_element(By.XPATH, storeSelection).send_keys('walmart')
        # self.driver.find_element(By.XPATH, storename).click()


    def newOrderTab(self):
        print("neworder tab in")
        self.driver.find_element(By.TAG_NAME,'body').send_keys(Keys.COMMAND + 't') 
        print("neworder tab done")
        self.driver.get(newOrderUrl)
        print("new order url")
        # self.driver.find_element(By.XPATH, newOrderNavBar).click()
        # assert newOrderUrl == self.driver.current_url()
    
    def searchStore(self):
        self.driver.find_element(By.XPATH, search).click()
        self.driver.find_element(By.XPATH, search).clear()
        self.driver.find_element(By.XPATH, search).sendkeys('walmart')
    
    def newStore(self):
        # TODO
        # Handle alert
        pass

    def tearDown(self):
        self.driver.quit()  



