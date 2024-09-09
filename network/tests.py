from django.test import TestCase
from network.models import Post

class TestPost(TestCase):

    def test_post_submission(self):
        # Register and log in
        self.register_and_log('tony','tony.fevrier@gmail.com','1234','1234')

        # Submit a post and verify its registering 
        self.client.post("/post", data={'post-content':'contenu du post'})
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertEqual(Post.objects.first().user, )
        self.assertEqual(Post.objects.first().text, 'contenu du post')
        self.assertEqual(Post.objects.first().likes, 0)
        
    def register_and_log(self, user, email, password, confirmation):
        self.client.post('/register',data={'username':user,
                                           'email':email,
                                           "password":password,
                                           'confirmation':confirmation})
        self.client.post('/login',data={'username':user,
                                        "password":password})
        
