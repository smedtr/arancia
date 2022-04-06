from django.test import TestCase
from django.test import override_settings
from blog.models import Post
from django.contrib.auth.models import User # Required to assign User as a borrower

# Create your tests here.
# tests.py
# Basis = https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

class PostModelTest(TestCase):
    
    @classmethod
    @override_settings(DEBUG=True) # Om sql debugging te hebben in test moet DEBUG op true staa
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        # Create published post
        Post.objects.create(
                title='Hoe laat je de poes beneden slapen',
                body= 'Het is een challenge om je poes beneden te laten slapen. Waarom zou je willen dat er gedurende de nacht een miauw is',
                author=test_user1,
                status='Published',                               
            )

        # Create 30 draft posts
        number_of_post_copies = 30
        for post_copy in range(number_of_post_copies):            
            the_author = test_user1 if post_copy % 2 else test_user2
            
            Post.objects.create(
                title='Test title ref',
                body= 'Test body ',
                author=the_author,                
            )

    def setUp(self):
        pass
        ## setUp() runs with every method execution
        
    @override_settings(DEBUG=True)
    def test_if_post_contains_correct_title(self):
        a_post = Post.objects.get(id=2)
        expected_object_title = 'Test title ref'
        self.assertEqual(str(a_post), expected_object_title)
  
    @override_settings(DEBUG=True)
    def test_if_user_can_login(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/blog/')

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    @override_settings(DEBUG=True)
    def test_if_post_is_available(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # Create published post
        Post.objects.create(
                title='Hoe laat je de poes beneden slapen',
                body= 'Het is een challenge om je poes beneden te laten slapen. Waarom zou je willen dat er gedurende de nacht een miauw is',
                author=1,
                status='Published',                               
        )
        response = self.client.get('/blog/')
        # Check if we have a post
        self.assertEqual(str(response.context['user']), 'testuser1')
       
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

    #def test_first_name_max_length(self):
    #    author = Author.objects.get(id=1)
    #    max_length = author._meta.get_field('first_name').max_length
    #    self.assertEqual(max_length, 100)

    #def test_object_name_is_last_name_comma_first_name(self):
    #    author = Author.objects.get(id=1)
    #    expected_object_name = f'{author.last_name}, {author.first_name}'
    #    self.assertEqual(str(author), expected_object_name)

    #def test_get_absolute_url(self):
    #    author = Author.objects.get(id=1)
    #    # This will also fail if the urlconf is not defined.
    #    self.assertEqual(author.get_absolute_url(), '/catalog/author/1')


