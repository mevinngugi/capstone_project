from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import CustomUser
from .models import Post
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token


# Create your tests here.
class BlogPostAPITestCase(TestCase):
    """Set up tests for posts and accounts model"""

    # Rename to setUp not setup
    def setUp(self):
        self.client = APIClient()

        # Create test user
        self.test_author = CustomUser.objects.create_user(username='test_author', email='test_author@gmail.com', password='testpassword')

        # Create test user's token
        self.token = Token.objects.create(user=self.test_author)

        self.test_post = Post.objects.create(
            title='Test Blog Post Title',
            content='This is a sample content',
            author=self.test_author,
            category='Tutorial'
        )

    # Test list all posts
    def test_list_post(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)

    # Test view post by id
    def test_post_detail(self):
        response = self.client.get(reverse('post-detail',
            kwargs={'pk': self.test_post.pk}
            ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.test_post.title)

    # Test create post with user who is not authenticated
    def test_create_post_with_UNAUTHENTICATED_user(self):
        response = self.client.post(reverse('post-list'), {
            'title': 'Test Post Title 2',
            'content': 'This is a test content for post 2',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test create post without mandatory fields
    def test_create_post_WITHOUT_mandatory_fields_AUTHENTICATED_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(reverse('post-list'), {
            'title': '',
            'content': 'This is a test content for post 2',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test create post with wrong category
    def test_create_post_with_WRONG_category(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(reverse('post-list'), {
            'title': 'Test Blog Post',
            'category': 'Wrong Category',
            'content': 'This is a test content for post 2',
        })
        # print("Response Data:", response.data['non_field_errors'])
        self.assertIn("The category must be one of the following: 'Tutorial, Project, Deployment'", response.data['non_field_errors'])

    def test_update_post_with_AUTHENTICATED_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.patch(reverse('post-detail', 
            kwargs={'pk': self.test_post.pk}),
            {
                'title': 'Updated Post Title',
                'category': 'Tutorial',
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post Title')

    def test_update_post_with_authenticated_WRONG_user(self):
        self.test_author2 = CustomUser.objects.create_user(username='test_author2', email='test_author2@gmail.com', password='testpassword2')

        self.token = Token.objects.create(user=self.test_author2)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.patch(reverse('post-detail', 
            kwargs={'pk': self.test_post.pk}),
            {
                'title': 'Updated Post Title',
                'category': 'Tutorial',
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_with_UNAUTHENTICATED_user(self):
        response = self.client.delete(reverse('post-detail', kwargs={'pk': self.test_post.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_with_AUTHENTICATED_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(reverse('post-detail', kwargs={'pk': self.test_post.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
