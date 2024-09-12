from django.test import TestCase
from network.models import Post

import json

class TestPost(TestCase):

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

    def test_view_profile(self):
        """Verify that the good informations are transmitted by view_profile"""
        # Submit two posts from two users
        self.submit_a_post('contenu du post')
        self.register_and_log('marine','marine.moyon@gmail.com','1234','1234')
        self.submit_a_post('contenu du post2')

        # Verify only the first post is transmitted for tony
        response = self.client.get('/profile/tony') 
        self.assertDictEqual(response.json()['user_stats'],{'followers_number':0,'following_number':0})
        self.assertEqual(len(response.json()['posts']),1)
        self.assertEqual(response.json()['posts'][0]['text'], 'contenu du post')

        # Verify only the second post is transmitted for marine
        response = self.client.get('/profile/marine') 
        self.assertDictEqual(response.json()['user_stats'],{'followers_number':0,'following_number':0})
        self.assertEqual(len(response.json()['posts']),1)
        self.assertEqual(response.json()['posts'][0]['text'], 'contenu du post2')
        
        
    def register_and_log(self, user, email, password, confirmation):
        self.client.post('/register',data={'username':user,
                                           'email':email,
                                           "password":password,
                                           'confirmation':confirmation})
        self.client.post('/login',data={'username':user,
                                        "password":password})
        
    def submit_a_post(self,content):
        self.client.post("/post", 
                         data=json.dumps({'post_content':content}),
                         content_type='application/json')
        
