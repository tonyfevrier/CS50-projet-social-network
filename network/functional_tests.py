from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options 

options = Options() 
options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"


class TestNetwork(StaticLiveServerTestCase): 
    
    def setUp(self):
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(3)
    
    def tearDown(self): 
        self.browser.quit()

    def test_network(self):
        # One user register log

        # He submits two posts appearing on the page 

        # He likes his second post and logout

        # A second user register, log and see the posts and the correct number of likes
        
        # He add a third post and likes all the posts and see the correct number of likes

        # He refresh the page All posts and see the correct number of likes
        pass

    def register_and_log(self):
        pass

    def logout(self):
        pass

    def submit_post(self):
        pass

    def like_post(self):
        pass

    def click_on_link(self):
        pass