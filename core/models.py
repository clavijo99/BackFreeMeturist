from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.conf import settings
import os
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from faker import Faker

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class UserManager(BaseUserManager):
    """ clase helper manejadora del modelo user """

    def create_user(self, email, password=None, **params):
        ''' crear usuario '''
        if not email:
            raise ValueError('the field email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **params)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        ''' crear usuario superusuario '''
        if not password:
            raise ValueError('the filed password is required')
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ model usuario """
    email = models.EmailField(max_length=255, verbose_name='Correo Electronico', unique=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    # fake_name = models.CharField(max_length=100, verbose_name='Nickname', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Usuario Activo')
    is_staff = models.BooleanField(default=False, verbose_name='Usuario Staff')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualizacion')
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, choices=(
        ("M", "Male"),
        ("F", "Female")
    ), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'


class Category(models.Model):
    """ model category """
    name = models.CharField(max_length=255, verbose_name='Nombre')
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Categoria'
        verbose_name_plural='Categorias'


class Site(models.Model):
    """ model site """
    name = models.CharField(max_length=255, verbose_name='Nombre')
    url = models.CharField(max_length=255, verbose_name='Enlace')
    location = models.CharField(max_length=255, verbose_name='Lugar')
    quality = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.CharField(max_length=500, verbose_name='Descripcion', null=True)
    address = models.CharField(max_length=500, verbose_name='direccion', null=True)

    image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sites')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_quality(self):
        comments = self.comment_set.all()
        print('lol')
        if comments.count() > 0:
            self.quality = comments.aggregate(models.Avg('quality'))['quality__avg']
        else:
            self.quality = 0
        self.save()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Sitio'
        verbose_name_plural='Sitios'

class Comment(models.Model):
    """ model comment """
    name = models.TextField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quality = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Comentario'
        verbose_name_plural='Comentarios'

class SocialNetwork(models.Model):
    """ model social network """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='social_networks')
    link = models.CharField(max_length=500, verbose_name="Enlace")
    type_social_network = models.CharField(max_length=30, verbose_name="Enlace", choices=(
        ("Facebook", "Facebook"),
        ("Instagram", "Instagram"),
        ("YouTube", "YouTube"),
        ("whatsApp", "whatsApp"),
    ))
   
   # def __str__(self):
     #   return self.name
    
    class Meta:
        verbose_name='RedSocalSitio'
        verbose_name_plural='RedesSocialesSitios'


class SiteImages(models.Model):
    """ model site image """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_images', verbose_name="Sitio")
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
   # def __str__(self):
    #    return self.name
    class Meta:
        verbose_name='ImagenSitio'
        verbose_name_plural='ImagenesSitios'


class Recommended(models.Model):
    """ model recommended """
    title = models.CharField(max_length=255, verbose_name="Titulo")
    content = models.TextField(verbose_name="Contenido")
    link = models.CharField(max_length=500, verbose_name="Enlace")
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    # def __str__(self):
    #    return self.name
    class Meta:
        verbose_name='PaginaRecomendada'
        verbose_name_plural='PaginasRecomendadas'

@receiver(post_save, sender=Comment)
def update_site_quality(sender, instance, **kwargs):
    instance.site.update_quality()

#funcion de generar nombres fake unida a la linea fake_name
#@receiver(pre_save, sender=User)
# def generate_fake_name(sender, instance, **kwargs):
#    if not instance.fake_name:
#        fake = Faker()
#        instance.fake_name = fake.name()


