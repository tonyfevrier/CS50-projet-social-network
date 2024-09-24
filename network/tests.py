from django.test import TestCase
from network.models import Post, User

import json

class TestNetwork(TestCase):

    def setUp(self):
        # Register and log in
        self.register_and_log('tony','tony.fevrier@gmail.com','1234','1234')

    def test_post_submission(self):
        # Submit a post and verify its registering 
        self.submit_a_post('contenu du post')
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertEqual(Post.objects.first().user.username, 'tony')
        self.assertEqual(Post.objects.first().text, 'contenu du post')
        self.assertEqual(Post.objects.first().likes, [])

    def test_view_some_posts(self):
        # Verify that the good informations are transmitted by view_posts
        self.submit_a_post('contenu du post')
        self.submit_a_post('contenu du post2')
        
        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(len(response.json()['posts']),2)
        self.assertEqual(response.json()['posts'][0]['username'], 'tony')
        self.assertEqual(response.json()['posts'][1]['username'], 'tony')
        self.assertIn('contenu du post2', [response.json()['posts'][0]['text'], response.json()['posts'][1]['text']])
        self.assertIn('contenu du post', [response.json()['posts'][0]['text'], response.json()['posts'][1]['text']]) 

    def test_views_one_post_after_liking(self):
        # Submit a post and like it
        self.submit_a_post("Hello")
        self.client.get("/likepost/1")
        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(response.json()["posts"][0]["likes"], 1)
        self.logout()

        # An other participant register log, see the posts
        self.register_and_log('marine','marine.moyon@gmail.com','1234','1234')
        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(response.json()["posts"][0]["likes"], 1)

        # He likes the post
        self.client.get("/likepost/1")
        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(response.json()["posts"][0]["likes"], 2)
        self.logout()
        
        # First user log and view posts
        self.login('tony', "1234")
        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(response.json()["posts"][0]["likes"], 2)    

    def test_views_some_posts_after_liking(self):
        # Submit 2 posts
        self.submit_a_post("Hello") 
        self.submit_a_post("knfnsf") 
        self.logout()

        # An other participant register and submit
        self.register_and_log('marine','m@gmail.com','1234','1234')
        self.submit_a_post('coucou')
        
        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(response.json()["posts"][0]["likes"], 0)
        self.assertEqual(response.json()["posts"][1]["likes"], 0)
        self.assertEqual(response.json()["posts"][2]["likes"], 0)

        # He likes the three posts
        self.client.get("/likepost/1")
        self.client.get("/likepost/2") 
        self.client.get("/likepost/3")

        self.assertListEqual(Post.objects.get(id=1).likes, ['marine'])
        self.assertListEqual(Post.objects.get(id=3).likes, ['marine'])
        self.assertListEqual(Post.objects.get(id=2).likes, ["marine"])


        response = self.client.get('/someposts/all?param1=1') 
        self.assertEqual(response.json()["posts"][0]["likes"], 1)
        self.assertEqual(response.json()["posts"][1]["likes"], 1)
        self.assertEqual(response.json()["posts"][2]["likes"], 1)
        self.logout()
        
        # First user log and view posts
        self.login('tony', "1234")
        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(response.json()["posts"][0]["likes"], 1)
        self.assertEqual(response.json()["posts"][1]["likes"], 1)
        self.assertEqual(response.json()["posts"][2]["likes"], 1) 

        # He likes posts    
        self.client.get("/likepost/1")
        self.client.get("/likepost/2")
        self.client.get("/likepost/3")

        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(response.json()["posts"][0]["likes"], 2)
        self.assertEqual(response.json()["posts"][1]["likes"], 2)
        self.assertEqual(response.json()["posts"][2]["likes"], 2) 

    def test_view_multiple_posts(self):
        """ Create a lot of tests and verify if only ten posts are transmitted"""
        for i in range(22):
            self.submit_a_post('contenu du post')

        response = self.client.get('/someposts/all?param1=1')
        self.assertEqual(len(response.json()['posts']),10)
        self.assertEqual(response.json()['previous'], False)
        self.assertEqual(response.json()['next'], True)

    def test_view_all_posts_with_multiple_users(self):
        """Several users create posts and thoses posts appear in all posts"""
        self.submit_a_post('contenu du post')
        self.register_log_and_submit('marine','m@gmail.com','1234','1234', 'coucou', "bonjour je m'appelle marine")
        self.register_log_and_submit('henri','h@gmail.com','1234','1234', 'hello')
        response = self.client.get('/someposts/all?param1=1') 
        self.assertIn('tony', [post['username'] for post in response.json()['posts']]) 

    def test_view_profile_posts(self):
        """Verify if only the following posts are printed when we click on following"""
        # Create four users including tony posting something 
        self.register_log_and_submit('marine','m@gmail.com','1234','1234', 'coucou', "bonjour je m'appelle marine")
        self.register_log_and_submit('henri','h@gmail.com','1234','1234', 'hello')
        self.register_log_and_submit('yann','y@gmail.com','1234','1234', 'buongiorno')
        self.login('tony','1234')

        # Click on following but nothing is sent
        response = self.client.get('/someposts/following?param1=1') 
        self.assertEqual(len(response.json()['posts']), 0)

        # Follow two among them
        self.client.get('/follow/marine')
        self.client.get('/follow/yann')

        # Click on following and verify the posts of marine and yann are sent but not those of henri
        response = self.client.get('/someposts/following?param1=1') 
        self.assertIn('coucou', [post['text'] for post in response.json()['posts']])
        self.assertIn("bonjour je m'appelle marine", [post['text'] for post in response.json()['posts']])
        self.assertIn('buongiorno', [post['text'] for post in response.json()['posts']])
        self.assertNotIn('hello', [post['text'] for post in response.json()['posts']])

    def test_view_profile(self):
        """Verify that the good informations are transmitted by view_profile"""
        # Submit two posts from two users
        self.submit_a_post('contenu du post')
        self.register_and_log('marine','marine.moyon@gmail.com','1234','1234')
        self.submit_a_post('contenu du post2')

        # Verify only the first post is transmitted for tony
        response = self.client.get('/profile/tony') 
        self.assertDictEqual(response.json()['user_stats'],{'followers_number':0,'following_number':0,'username':'tony'})
        self.assertEqual(len(response.json()['posts']),1)
        self.assertEqual(response.json()['posts'][0]['text'], 'contenu du post')
        self.assertEqual(response.json()['userisowner'], False)

        # Verify only the second post is transmitted for marine
        response = self.client.get('/profile/marine') 
        self.assertDictEqual(response.json()['user_stats'],{'followers_number':0,'following_number':0,'username':'marine'})
        self.assertEqual(len(response.json()['posts']),1)
        self.assertEqual(response.json()['posts'][0]['text'], 'contenu du post2')
        self.assertEqual(response.json()['userisowner'], True)

    def test_view_profile_posts_after_liking(self):
        # Submit a post and like it
        self.submit_a_post("Hello")
        self.client.get("/likepost/1")
        response = self.client.get('/profile/tony') 
        self.assertEqual(response.json()["posts"][0]["likes"], 1)

        # An other participant register log, see the posts
        self.register_and_log('marine','marine.moyon@gmail.com','1234','1234')   
        response = self.client.get('/profile/tony')  
        self.assertEqual(response.json()["posts"][0]["likes"], 1)

        # He likes the post
        self.client.get("/likepost/1")        
        response = self.client.get('/profile/tony')  
        self.assertEqual(response.json()["posts"][0]["likes"], 2)

    def test_follow_or_infollow(self):
        self.register_and_log('marine','marine.moyon@gmail.com','1234','1234')

        # Make a get request to follow marine
        self.client.get('/follow/tony')

        # Verify the database has been correctly updated
        tony = User.objects.get(username='tony')
        marine = User.objects.get(username='marine')
        self.assertIn('tony',marine.following)
        self.assertIn('marine',tony.followers)

        # The same to unfollow
        self.client.get('/follow/tony')
        tony = User.objects.get(username='tony')
        marine = User.objects.get(username='marine')
        self.assertNotIn('tony',marine.following)
        self.assertNotIn('marine',tony.followers)

    def test_edit_post(self):
        """Create a post, edit it and verify the database has been correctly modified"""
        self.submit_a_post('Hello')
        self.assertEqual(Post.objects.first().text, 'Hello')
        self.client.post('/editpost/1', data=json.dumps({'content':"Hello man"}), content_type='application/json')
        self.assertEqual(Post.objects.first().text, 'Hello man')
        self.submit_a_post('Hello again')
        self.client.post('/editpost/1', data=json.dumps({'content':"Hello man My name is Ben"}), content_type='application/json')
        self.assertEqual(Post.objects.first().text, 'Hello man My name is Ben')
        self.client.post('/editpost/2', data=json.dumps({'content':"Hello again woman"}), content_type='application/json')
        self.assertEqual(Post.objects.get(id=2).text, 'Hello again woman')

    def test_like_post(self): 
        # Create a post and like it
        self.submit_a_post('Hello')
        self.assertListEqual(Post.objects.first().likes, [])
        self.client.get("/likepost/1")   

        # A second user like it, data is correctly registered and sent.    
        self.register_and_log('marine','marine.moyon@gmail.com','1234','1234')
        response = self.client.get("/likepost/1")
        self.assertListEqual(Post.objects.first().likes, ['tony', 'marine'])
        self.assertEqual(response.json()["post"]["likes"], 2)

        # A user dislikes it, date is correcly registered and sent.
        response = self.client.get("/likepost/1")
        self.assertListEqual(Post.objects.first().likes, ['tony']) 
        self.assertEqual(response.json()["post"]["likes"], 1)

    def test_like_post_unlogged(self):
        self.submit_a_post('test')
        self.logout()

        # Try to like while unlogged
        response = self.client.get("/likepost/1")
        self.assertEqual(response.json()['error'], 'You must log in before liking')
    
    # Utils

    def register_and_log(self, user, email, password, confirmation):
        self.client.post('/register',data={'username':user,
                                           'email':email,
                                           "password":password,
                                           'confirmation':confirmation})
        self.client.post('/login',data={'username':user,
                                        "password":password})
        
    def login(self, user, password): 
        self.client.post('/login',data={'username':user,
                                        "password":password})
        
    def submit_a_post(self,content):
        self.client.post("/post", 
                         data=json.dumps({'post_content':content}),
                         content_type='application/json')
    
    def logout(self):
        self.client.get('/logout')

    def register_log_and_submit(self,  user, email, password, confirmation, *posts):
        self.register_and_log(user, email, password, confirmation)
        for post in posts:
            self.submit_a_post(post)
        self.logout()
        
