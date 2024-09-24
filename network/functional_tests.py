from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time 

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
        self.browser.get(self.live_server_url)
        self.register_and_log("tony", "t@gmail.com", "1234")

        # He submits two posts appearing on the page 
        self.submit_post("Test1")
        self.submit_post("Test2")

        posts = self.browser.find_elements(By.CLASS_NAME, "post-element")
        self.assertEqual(len(posts), 2)
        self.assertSetEqual({"Test1","Test2"}, set(self.get_post_informations(post)["text"] for post in posts))
        self.assertSetEqual({"tony"}, set(self.get_post_informations(post)["username"] for post in posts)) 
        self.assertSetEqual({'0'}, set(self.get_post_informations(post)["likes"] for post in posts)) 

        # He likes his second post and logout
        self.like_post(2)
        posts = self.browser.find_elements(By.CLASS_NAME, "post-element")
        self.assertEqual('1', self.get_post_informations(posts[0])["likes"])
        self.logout() 

        # A second user register, log and see the posts and the correct number of likes
        self.register_and_log("marine", "m@gmail.com", "1234")
        posts = self.browser.find_elements(By.CLASS_NAME, "post-element")
        self.assertEqual(len(posts), 2)
        self.assertSetEqual({"Test1","Test2"}, set(self.get_post_informations(post)["text"] for post in posts))
        self.assertSetEqual({"tony"}, set(self.get_post_informations(post)["username"] for post in posts)) 
        self.assertSetEqual({'0', '1'}, set(self.get_post_informations(post)["likes"] for post in posts)) 
        
        # He add a third post and likes all the posts and see the correct number of likes
        self.submit_post("Test3")
        posts = self.browser.find_elements(By.CLASS_NAME, "post-element")
        self.assertSetEqual({'0', '1'}, set(self.get_post_informations(post)["likes"] for post in posts)) 

        # He refresh the page All posts and see the correct number of likes
        self.click_on_link(By.ID, "allposts-btn")
        posts = self.browser.find_elements(By.CLASS_NAME, "post-element") 
        self.assertEqual('1', self.get_post_informations(posts[1])["likes"])

        #He likes the first and the second post and see the correct number of likes
        self.like_post(2)
        self.like_post(1)
        posts = self.browser.find_elements(By.CLASS_NAME, "post-element") 
        self.assertEqual('2', self.get_post_informations(posts[1])["likes"])
        self.assertEqual('1', self.get_post_informations(posts[2])["likes"])

        # He then dislike the second post
        self.like_post(2)
        self.assertEqual('1', self.get_post_informations(posts[1])["likes"])

        # He refresh the page All posts and see the correct number of likes
        self.click_on_link(By.ID, "allposts-btn")
        posts = self.browser.find_elements(By.CLASS_NAME, "post-element") 
        self.assertEqual('1', self.get_post_informations(posts[1])["likes"])

    def register_and_log(self, username, email, password):
        self.click_on_link(By.ID, "register")  
        self.browser.find_element(By.NAME, "username").send_keys(username)
        self.browser.find_element(By.NAME, "email").send_keys(email)
        self.browser.find_element(By.NAME, "password").send_keys(password)
        self.browser.find_element(By.NAME, "confirmation").send_keys(password)
        self.browser.find_element(By.CLASS_NAME, "btn-primary").send_keys(Keys.ENTER)
        time.sleep(2)
 
    def logout(self):
        self.browser.find_element(By.ID, "logout").send_keys(Keys.ENTER)
        time.sleep(2)

    def submit_post(self, text):
        self.browser.find_element(By.ID, "textarea-content").send_keys(text)
        self.browser.find_element(By.ID, "submit-post").send_keys(Keys.ENTER)
        time.sleep(2)

    def like_post(self, id): 
        self.browser.find_element(By.ID, f"post-{id}").send_keys(Keys.ENTER)
        time.sleep(2)

    def click_on_link(self, literal, name):
        link = self.browser.find_element(literal, name)
        link.send_keys(Keys.ENTER)
        time.sleep(2)
        
    def get_post_informations(self, post):
        return {"username":post.find_element(By.CLASS_NAME, "user-btn").text,
                "text":post.find_element(By.CLASS_NAME, "post-text").text,
                "date":post.find_element(By.CLASS_NAME, "post-date").text,
                "likes":post.find_element(By.CLASS_NAME, "post-likes").text
                }
    
        