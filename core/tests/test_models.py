from django.test import TestCase
from core.models import Category, Site, Comment
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from location.tests.utils import sample_category, sample_site


def sampleUser(email='test@test.com', password='password'):
    ''' crea un usuario '''
    return get_user_model().objects.create_user(email=email, password=password)


class TestsModels(TestCase):
    """ purebas para los modelos """

    def test_create_user(self):
        ''' prueba crear modelo usuario '''
        email = 'test@test.com'
        password = 'test124'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        ''' probar normalizacion de correo '''
        email = 'test@TEST.COM'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_user_without_email(self):
        ''' prueba usuario sin correo '''
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(email='', password='test')

    def test_create_superuser(self):
        ''' crear super usuario '''
        email = 'test@test.com'
        password = 'test1234'
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_without_password(self):
        ''' crear super usuario sin contrase~na '''
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_superuser(email='test@test.com', password=None)

    def test_listed_users(self):
        ''' listar usuarios '''
        user = get_user_model().objects.create_user(email='test@test.com', password='password')
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, user.email)

    def test_category_str(self):
        """
        test category str
        """
        category = sample_category()
        self.assertEqual(str(category), category.name)

    def test_site_str(self):
        """
        test site str
        """
        site = sample_site()
        self.assertEqual(str(site), site.name)

    def test_comment_str(self):
        """
        test comment str
        """
        user = get_user_model().objects.create_user(email='test@test.com', password='test124')
        site = sample_site()
        comment = Comment.objects.create(name='comment 1', site=site, user=user)
        self.assertEqual(str(comment), comment.name)
