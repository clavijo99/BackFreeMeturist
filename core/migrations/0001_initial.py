# Generated by Django 4.0.4 on 2023-06-30 20:27

import core.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Correo Electronico')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('fake_name', models.CharField(blank=True, max_length=100, verbose_name='Nickname')),
                ('is_active', models.BooleanField(default=True, verbose_name='Usuario Activo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Usuario Staff')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha Actualizacion')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=core.models.upload_to)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='Recommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Titulo')),
                ('content', models.TextField(verbose_name='Contenido')),
                ('link', models.CharField(max_length=500, verbose_name='Enlace')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('url', models.CharField(max_length=255, verbose_name='Enlace')),
                ('location', models.CharField(max_length=255, verbose_name='Lugar')),
                ('quality', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('description', models.CharField(max_length=500, null=True, verbose_name='Descripcion')),
                ('address', models.CharField(max_length=500, null=True, verbose_name='direccion')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.upload_to)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=500, verbose_name='Enlace')),
                ('type_social_network', models.CharField(choices=[('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('YouTube', 'YouTube'), ('Redis', 'Redis')], max_length=30, verbose_name='Enlace')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_networks', to='core.site')),
            ],
        ),
        migrations.CreateModel(
            name='SiteImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.upload_to)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_images', to='core.site')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('quality', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.site')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
