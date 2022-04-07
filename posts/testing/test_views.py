# posts/tests/test_views.py

# Create your tests here.

from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from posts.models import Article
from django.contrib.auth.models import User  # Required to assign User as author

#
# Create your tests here.
# Basis = https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
# Om alleen deze module te testen : python manage.py test posts.testing of
#                                   python manage.py test posts.testing.test_views 
#

class ArticleListViewTest(TestCase):
   
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

        # Create 10 draft posts
        number_of_article_copies = 10
        for article_copy in range(number_of_article_copies):
            the_author = test_user1 if article_copy % 2 else test_user2

            Article.objects.create(
                title='Title of test article with status draft.',
                text='Body of test article with status draft.',
                author=the_author,
            )

        # Create 10 published posts
        number_of_article_copies = 12
        for article_copy in range(number_of_article_copies):
            the_author = test_user1 if article_copy % 2 else test_user2

            Article.objects.create(
                title='Title of test article with status draft.',
                text='Body of test article with status draft.',
                author=the_author,
                status='published',
            )

    def setUp(self):
        pass
        ## setUp() runs with every method execution

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self): # reverse is de name in de url.conf
        response = self.client.get(reverse('posts:article-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('posts:article-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/articles/article_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('posts:article-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['articles']), 5)

    def test_lists_all_articles(self):
        # Get third page and confirm it has (exactly) remaining 3 items
        # There have been 13 articles created in published state
        response = self.client.get(reverse('posts:article-list')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['articles']), 3)

class ArticleAddViewTest(TestCase):
   
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

    def setUp(self):
        pass
        ## setUp() runs with every method execution

    def test_add_url_exists_at_desired_location(self):
        response = self.client.get('/articles/add/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self): # reverse is de name in de url.conf
        response = self.client.get(reverse('posts:article-new'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('posts:article-new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/articles/article_edit.html')

    
