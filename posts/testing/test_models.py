# posts/tests/test_models.py

# Create your tests here.

from django.test import TestCase
from django.test import override_settings
from posts.models import Article
from django.contrib.auth.models import User  # Required to assign User as author

# Create your tests here.
# tests.py
# Basis = https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
# Om alleen deze module te testen : python manage.py test posts.testing of
#                                   python manage.py test posts.testing.test_models 

class ArticleModelTest(TestCase):

    @classmethod
    # Om sql debugging te hebben in test moet DEBUG op true staa
    @override_settings(DEBUG=True)
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        # Create two users
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create Article
        Article.objects.create(
            title='Eerste artikel',
            text='Het is een challenge om je poes beneden te laten slapen. Waarom zou je willen dat er gedurende de nacht een miauw is',
            author=test_user1,
            status='published',
        )

        # Create 30 draft posts
        number_of_article_copies = 30
        for article_copy in range(number_of_article_copies):
            the_author = test_user1 if article_copy % 2 else test_user2

            Article.objects.create(
                title='Test title ref',
                text='Test body ',
                author=the_author,
            )

    def setUp(self):
        pass
        ## setUp() runs with every method execution

    
    def test_title_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_slug_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200) 

    def test_get_absolute_url(self):
        article = Article.objects.get(id=1)
        created_url = str(article.id) + '-' + \
            article.slug + '/'
        # This will also fail if the urlconf is not defined.
        self.assertEqual(article.get_absolute_url(), '/articles/' + created_url)

    def test_if_published_article_is_available(self):
        #self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        author = User.objects.get(username='testuser1')
        # Create published article
        article_title = 'Hoe laat je de poes beneden slapen'
        article_text = 'Het is een challenge om je poes beneden te laten slapen. Waarom zou je willen dat er gedurende de nacht een miauw is'
        Article.objects.create(
            title=article_title,
            text=article_text,
            author=author,
            status='published',
        )
        # Check if the article was created
        created_article = Article.objects.get(title=article_title)
        self.assertEqual(created_article.title, article_title)

        # Check that we got a response "success"
        created_url = str(created_article.id) + '-' + \
            created_article.slug + '/'
        response = self.client.get('/articles/' + created_url)
        self.assertEqual(response.status_code, 200)

        # Check if we have a post
        #self.assertEqual(str(response.context['user']), 'testuser1')

    def test_if_draft_article_is_not_shown(self):
        #self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        author = User.objects.get(username='testuser1')
        # Create published article
        article_title = 'Dit zou niet mogen getoond worden'
        article_text = 'Het is een challenge om je poes beneden te laten slapen. Waarom zou je willen dat er gedurende de nacht een miauw is'
        Article.objects.create(
            title=article_title,
            text=article_text,
            author=author,
            status='draft',
        )
        # Check if the article was created
        created_article = Article.objects.get(title=article_title)
        self.assertEqual(created_article.title, article_title)

        # Check that we got a response 404 "NotFound"
        created_url = str(created_article.id) + '-' + \
            created_article.slug + '/'
        response = self.client.get('/articles/' + created_url)
        self.assertEqual(response.status_code, 404)

       

         