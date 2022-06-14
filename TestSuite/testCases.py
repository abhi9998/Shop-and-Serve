import time
import unittest
from signUpPage import signUpPage
from loginPage import loginPage
from lib2to3.pgen2 import driver
from newOrderPage import newOrder
from addStorePage import addStorePage
import HTMLTestRunner

def test_TC001_login():
    loginPage.setUp(self=driver)
    loginPage.loginAsUser(self=driver)
    print("TC001_passed")
    # loginPage.tearDown(self=driver)
    # loginPage.handleToastifyAlert(self=driver)

def test_TC002_verifyHomePage():
    loginPage.verifyHomePage(self=driver)
    # loginPage.tearDown(self=driver)
    print("TC002_passed")

def test_TC007_signOutFailed():
    # signUpPage.setUp(self=driver)
    signUpPage.signOutUser(self=driver)
    signUpPage.tearDown(self=driver)
    print("TC007_Passed")

def test_TC003_adminLogin():
    # loginPage.switchWindow(self=driver)
    loginPage.setUpAdmin(self=driver)
    loginPage.loginAsAdmin(self=driver)
    loginPage.tearDown(self=driver)
    print("TC003_passed")

def test_TC004_loginFailed():
    loginPage.setUp(self=driver)
    loginPage.loginFailedAsUser
    loginPage.tearDown(self=driver)
    print("TC004_Passed")

def test_TC005_signUpNewUser():
    signUpPage.setUp(self=driver)
    signUpPage.userSignUp(self=driver)
    signUpPage.tearDown(self=driver)
    print("TC005_Passed")

def test_TC006_signoutUser():
    signUpPage.setUp(self=driver)
    loginPage.loginAsUser(self=driver)
    signUpPage.signOutUser(self=driver)
    signUpPage.tearDown(self=driver)
    print("TC006_Passed")

def test_TC008_addStore():
    loginPage.setUpAdmin(self=driver)
    loginPage.loginAsAdmin(self=driver)
    addStorePage.addStore(self=driver)
    addStorePage.tearDown(self=driver)
    print("TC008_Passed")

def test_TC009_createNewOrder():
    loginPage.setUp(self=driver)
    loginPage.loginAsUser(self=driver)
    time.sleep(5)
    # newOrder.wait(self=driver)
    newOrder.newOrderNewTab(self=driver)
    newOrder.selectStore(self=driver)
    loginPage.tearDown(self=driver)
    # newOrder.newOrderTab(self=driver)
    # newOrder.setUpNewOrder(self=driver)
    # newOrder.newOrderTab(self=driver)
    # newOrder.newOrderTab(self=driver)
    # newOrder.searchStore(self=driver)

def test_TC010_testcreationAssert():
    assert 1==2
    # newOrder.newOrderNewTab(self=driver)
    # newOrder.selectStore(self=driver)
    # loginPage.tearDown(self=driver)


# if __name__ == '__main__':
#     unittest.main(testRunner=testRunner)

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='..Reports'))
