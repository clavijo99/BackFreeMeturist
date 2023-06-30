from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from core import models
from location.serializer import CategorySerializer
from django.contrib.auth import get_user_model
from location.tests.utils import sample_category, get_temporary_image
from django.core.files.uploadedfile import SimpleUploadedFile

CATEGORY_URL = reverse('location:category-list')


def retrieve_category_url(id_category):
    return reverse('location:category-detail', args=[id_category])


class PublicCategoryApiTest(TestCase):
    """
    class test category model
     """

    def setUp(self):
        self.client = APIClient()

    def test_category_list(self):
        """
        test get list cities
        """
        sample_category(name='category one')
        sample_category(name='category two')

        countries = models.Category.objects.all()
        serializer = CategorySerializer(countries, many=True)

        response = self.client.get(CATEGORY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_retrieve_category(self):
        """
        test get category by id
        """
        category = sample_category()
        url = retrieve_category_url(category.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)

    def test_update_unauthorized(self):
        """
        test retrieve category if not authenticated
        """
        category = sample_category()
        image = get_temporary_image(name="image_2.jpg")
        url = retrieve_category_url(category.id)
        payload = {
            'name': 'category test',
            'image': image
        }
        response = self.client.put(url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryApiTest(TestCase):
    """
    test create category if is admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(email='test@test.com', name='test', password='test123')
        self.client.force_authenticate(user=self.admin)

    def test_create_category(self):
        """
        test create category user admin
        """
        image = get_temporary_image()
        payload = {
            'name': 'Test Image',
            'image': image
        }
        response = self.client.post(CATEGORY_URL, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], payload['name'])

    def test_update_authorized(self):
        """
        test retrieve category if authenticated is admin
        """
        category = sample_category()
        url = retrieve_category_url(category.id)
        image = get_temporary_image()
        payload = {
            'name': 'category test',
            'image': image
        }
        response = self.client.put(url, payload)
        category = models.Category.objects.get(pk=response.data['id'])
        serializer = CategorySerializer(category, many=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], serializer.data['id'])

    def test_delete_authorized(self):
        """
        test delete category if authenticated is admin
        """
        category = sample_category()
        url = retrieve_category_url(category.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        exists_category = models.Category.objects.filter(pk=category.id).exists()
        self.assertFalse(exists_category)


class PrivateCategoryApiTestNotAmin(TestCase):
    """
    validate private url if not admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@user.com', name='user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_delete_forbidden(self):
        """
        test retrieve category if not authenticated
        """
        category = sample_category()
        url = retrieve_category_url(category.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
