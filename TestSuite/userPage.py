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
