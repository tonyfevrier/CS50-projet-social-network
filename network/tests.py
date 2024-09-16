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
        self.assertEqual(Post.objects.first().likes, 0)

    def test_view_some_posts(self):
        # Verify that the good informations are transmitted by view_posts
        self.submit_a_post('contenu du post')
        self.submit_a_post('contenu du post2')
        
        response = self.client.get('/someposts/all')
        self.assertEqual(len(response.json()),2)
        self.assertEqual(response.json()[0]['username'], 'tony')
        self.assertEqual(response.json()[1]['username'], 'tony')
        self.assertIn('contenu du post2', [response.json()[0]['text'], response.json()[1]['text']])
        self.assertIn('contenu du post', [response.json()[0]['text'], response.json()[1]['text']]) 

    def test_view_profile_posts(self):
        """Verify if only the following posts are printed when we click on following"""
        # Create four users including tony posting something 
        self.register_log_and_submit('marine','m@gmail.com','1234','1234', 'coucou', "bonjour je m'appelle marine")
        self.register_log_and_submit('henri','h@gmail.com','1234','1234', 'hello')
        self.register_log_and_submit('yann','y@gmail.com','1234','1234', 'buongiorno')
        self.login('tony','1234')

        # Click on following but nothing is sent
        response = self.client.get('/someposts/following') 
        self.assertEqual(len(response.json()), 0)

        # Follow two among them
        self.client.get('/follow/marine')
        self.client.get('/follow/yann')

        # Click on following and verify the posts of marine and yann are sent but not those of henri
        response = self.client.get('/someposts/following') 
        self.assertIn('coucou', [post['text'] for post in response.json()])
        self.assertIn("bonjour je m'appelle marine", [post['text'] for post in response.json()])
        self.assertIn('buongiorno', [post['text'] for post in response.json()])
        self.assertNotIn('hello', [post['text'] for post in response.json()])



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
        
