from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.conf import settings
import os
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _
#from faker import Faker

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
    email = models.EmailField(_('Correo Electronico'), max_length=255, unique=True)
    name = models.CharField(_('Nombre'), max_length=100)
    # fake_name = models.CharField(max_length=100, verbose_name='Nickname', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Usuario Activo')
    is_staff = models.BooleanField(default=False, verbose_name='Usuario Staff')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualizacion')
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    phone = models.CharField(_('Telefono'), max_length=100, blank=True, null=True)
    nationality = models.CharField(_('Nacionalidad'), max_length=100, blank=True, null=True)
    gender = models.CharField(_('Genero'), max_length=100, choices=(
        ("M", "Masculino"),
        ("F", "Femenino")
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
    name = models.CharField(_('Nombre'), max_length=255, )
    image = models.ImageField(_('Imagen'), upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Categoria'
        verbose_name_plural='Categorias'


class Site(models.Model):
    """ model site """
    name = models.CharField(_('Sitio'), max_length=255, )
    url = models.CharField(_('Enlace'), max_length=255, )
    location = models.CharField(_('Lugar'), max_length=255, )
    quality = models.DecimalField(_('Calificación'), max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.CharField(_('Descripcion'), max_length=500, null=True)
    address = models.CharField(_('Dirección'), max_length=500, null=True)

    image = models.ImageField(_('Imagen'), upload_to=upload_to, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sites', verbose_name="Categoria")
    price = models.FloatField(_('Precio'),  default=0.0)

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
    name = models.TextField(_('Comentario'))
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Sitio')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    quality = models.DecimalField(_('Calificación'), max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

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
    link = models.CharField(_('Enlace'), max_length=500, )
    type_social_network = models.CharField(_('Tipo'), max_length=30, choices=(
        ("Facebook", "Facebook"),
        ("Instagram", "Instagram"),
        ("YouTube", "YouTube"),
        ("whatsApp", "whatsApp"),
    ))
   

    class Meta:
        verbose_name='Red Socal Sitio'
        verbose_name_plural='Redes Sociales Sitios'


class SiteImages(models.Model):
    """ model site image """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_images', verbose_name="Sitio")
    image = models.ImageField(_('Imagen'), upload_to=upload_to, blank=True, null=True)

    class Meta:
        verbose_name='Imagen Del Sitio'
        verbose_name_plural='Imagenes De Los Sitios'


class Recommended(models.Model):
    """ model recommended """
    title = models.CharField(_('Titulo'), max_length=255)
    content = models.TextField(_('Contenido'))
    link = models.CharField(_('Enlace'), max_length=500)
    image = models.ImageField(_('Imagen'), upload_to=upload_to, blank=True, null=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Pagina Recomendada'
        verbose_name_plural='Paginas Recomendadas'

@receiver(post_save, sender=Comment)
def update_site_quality(sender, instance, **kwargs):
    instance.site.update_quality()





#funcion de generar nombres fake unida a la linea fake_name
#@receiver(pre_save, sender=User)
# def generate_fake_name(sender, instance, **kwargs):
#    if not instance.fake_name:
#        fake = Faker()
#        instance.fake_name = fake.name()


