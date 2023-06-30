from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core import models
from location.tests.utils import sample_site
from register.serializer import CommentListSerializer, CommentSerializer

COMMENT_URL = reverse('register:comment-list')


def detail_url(id_comment):
    return reverse('register:comment-detail', args=[id_comment])


def sample_register_comment(user, site, **kwargs):
    payload = {
        'name': 'comment site',
        'site': site
    }
    payload.update(kwargs)
    return models.Comment.objects.create(user=user, **payload)


class PublicRegisterApiTest(TestCase):
    """ tests api by access public """

    def setUp(self):
        self.client = APIClient()

    def test_list_unauthorized(self):
        """ test get list people registered """
        response = self.client.get(COMMENT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRegisterApiTest(TestCase):
    """ tests api by access private """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@test.com', name='test', password='test1234')
        self.client.force_authenticate(user=self.user)

    def test_create_success(self):
        """ register comment """
        site = sample_site(name='site 1')
        payload = {
            'name': 'comment site',
            'site': site.pk
        }
        response = self.client.post(COMMENT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertIn('name', response.data)

    def test_listed_by_user(self):
        """ test list comment registered by user """
        site = sample_site('site 1')
        sample_register_comment(user=self.user, site=site, name='comment site test')

        user1 = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        sample_register_comment(user=user1, site=site, name='test')

        response = self.client.get(COMMENT_URL)
        comments = models.Comment.objects.filter(user=self.user)
        serializer = CommentListSerializer(comments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_retrieve_comment(self):
        """ test retrieve comment by id """
        site = sample_site('site 1')
        comment = sample_register_comment(user=self.user, site=site, name='comment 1')
        serializer = CommentListSerializer(comment)
        url = detail_url(comment.id)
        response = self.client.get(url)
        self.assertEqual(response.data['id'], serializer.data['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_comment_by_not_user(self):
        """ test retrieve comment when comment not belong to user """
        site = sample_site('site 1')
        user = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        comment = sample_register_comment(user=user, site=site, name='comment 1')
        url = detail_url(comment.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment(self):
        """ test update comment by id """
        site = sample_site('site 1')
        comment = sample_register_comment(user=self.user, site=site, name='comment 1')
        payload = {
            'name': 'comment 2 edit',
            'site': site.id
        }
        url = detail_url(comment.id)
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], payload['name'])

    def test_update_comment_by_not_user(self):
        """ test update comment when comment not belong to user """
        site = sample_site('site 1')
        user = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        comment = sample_register_comment(user=user, site=site, name='comment 1')
        url = detail_url(comment.id)
        payload = {
            'name': 'comment 2 edit',
            'site': site.pk
        }
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment(self):
        """ test delete comment by id """
        site = sample_site('site 1')
        comment = sample_register_comment(user=self.user, site=site, name='comment 1')
        url = detail_url(comment.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_by_not_user(self):
        """ test delete comment when comment not belong to user """
        site = sample_site('site 1')
        user = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        comment = sample_register_comment(user=user, site=site, name='comment 1')
        url = detail_url(comment.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_comments_by_site(self):
        site = sample_site('site 1')
        site2 = sample_site('site 2')
        user = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        # make a 3 comments
        sample_register_comment(user=self.user, site=site, name='comment 1')
        sample_register_comment(user=self.user, site=site, name='comment 2')
        sample_register_comment(user=user, site=site2, name='comment 3')

        comments = models.Comment.objects.filter(site__id=site.pk)
        serializer = CommentSerializer(comments, many=True)

        url = reverse('register:comments-list', kwargs={'site_id': site.pk})

        response = self.client.get(url)
        self.assertEqual(response.data, serializer.data)
