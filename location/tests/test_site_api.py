from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from location.serializer import SiteSerializer
from django.contrib.auth import get_user_model
from core import models
from location.tests.utils import sample_category, sample_site, get_temporary_image

SITE_URL = reverse('location:site-list')


def retrieve_site_url(id_site):
    return reverse('location:site-detail', args=[id_site])


class PublicSiteApiTest(TestCase):
    """
    class test site model
     """

    def setUp(self):
        self.client = APIClient()

    def test_site_list(self):
        """
        test get list sites
        """
        category = sample_category()
        sample_site(name='site 1', url='https://www.test1.com/', location='location 1', quality=5.0)
        sample_site(name='site 2', url='https://www.test2.com/', location='location 2', quality=4.2)

        sites = models.Site.objects.all()
        serializer = SiteSerializer(sites, many=True)

        response = self.client.get(SITE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_retrieve_site(self):
        """
        test get site by id
        """
        category = sample_category()
        site = sample_site()
        url = retrieve_site_url(site.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)

    def test_update_unauthorized(self):
        """
        test retrieve site if not authenticated
        """
        category = sample_category()
        site = sample_site()
        url = retrieve_site_url(site.id)
        image = get_temporary_image()
        payload = {
            'name': 'site test',
            'url': 'https://www.test-edit.com/',
            'location': 'location test edit',
            'quality': 3.0,
            'image': image,
            'category': category.pk
        }
        response = self.client.put(url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSiteApiTest(TestCase):
    """
    test create site if is admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(email='test@test.com', name='test', password='test123')
        self.client.force_authenticate(user=self.admin)

    def test_create_site(self):
        """
        test create site user admin
        """
        category = sample_category()
        image = get_temporary_image()
        payload = {
            'name': 'site test',
            'url': 'https://www.test-edit.com/',
            'location': 'location test edit',
            'quality': 3.0,
            'image': image,
            'category': category.pk
        }
        response = self.client.post(SITE_URL, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], payload['name'])

    def test_update_authorized(self):
        """
        test retrieve site if authenticated is admin
        """
        category = sample_category()
        site = sample_site()
        url = retrieve_site_url(site.id)
        image = get_temporary_image()
        payload = {
            'name': 'site test edit',
            'url': 'https://www.test-edit.com/',
            'location': 'location test edit',
            'quality': 3.0,
            'image': image,
            'category': category.pk
        }
        response = self.client.put(url, payload, format='multipart')
        site = models.Site.objects.get(pk=response.data['id'])
        serializer = SiteSerializer(site, many=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], serializer.data['name'])

    def test_delete_authorized(self):
        """
        test delete site if authenticated is admin
        """
        category = sample_category()
        site = sample_site()
        url = retrieve_site_url(site.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        exists_site = models.Site.objects.filter(pk=site.id).exists()
        self.assertFalse(exists_site)


class PrivateSiteApiTestNotAmin(TestCase):
    """
    validate private url if not admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@user.com', name='user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_delete_forbidden(self):
        """
        test retrieve site if not authenticated
        """
        site = sample_site()
        url = retrieve_site_url(site.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
