from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from articles.models.article import Article
from django.test.runner import DiscoverRunner

class NoSQLTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass
    def teardown_databases(self, old_config, **kwargs):
        pass

class NoSQLTestCase(APITestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass

class ArticleListAPITestCase(NoSQLTestCase):
    def setUp(self):
        self.articles_data = [
            {
                "title": "Sample Article 1",
                "url": "https://example.com/sample1",
                "authors": [{"name": "John Doe"}],
                "categories": ["Technology"],
                "read_time_in_minutes": 5,
                "publish_date": "2024-02-06T12:00:00Z"
            },
            {
                "title": "Sample Article 2",
                "url": "https://example.com/sample2",
                "authors": [{"name": "Jane Doe"}],
                "categories": ["Science"],
                "read_time_in_minutes": 8,
                "publish_date": "2024-02-06T13:30:00Z"
            }
        ]


    def test_create_update_articles(self):
        url = reverse('article-list')
        response = self.client.post(url, self.articles_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'Articles Created/Updated Successfully.')

        # Check if articles are created/updated in the database
        for article_data in self.articles_data:
            article = Article.objects.get(url=article_data['url'])
            self.assertEqual(article.title, article_data['title'])
            # Add more assertions for other fields

    def test_invalid_request(self):
        invalid_data = [
           {
                "title": "Invalid Article",
                "url": "https://example.com/invalid",
                "categories": [{"term":"Technologies"}],
                "read_time_in_minutes": 5,
                "publish_date": "2024-02-06T12:00:00Z"
            }
        ]

        url = reverse('article-list')
        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)
        self.assertIn('errors', response.data)

        # Ensure that no articles are created/updated in the database
        for article_data in invalid_data:
            with self.assertRaises(Article.DoesNotExist):
                Article.objects.get(url=article_data['url'])
