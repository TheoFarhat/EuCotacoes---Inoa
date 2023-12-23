# Generated by Django 5.0 on 2023-12-23 20:26

import core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=50)),
                ('age', models.IntegerField()),
                ('cpf', models.IntegerField(unique=True, validators=[core.validators.validate_cpf])),
                ('email', models.EmailField(max_length=254, unique=True, validators=[core.validators.validate_email])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id_asset', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=50)),
                ('symbol', models.TextField(max_length=50)),
                ('price', models.FloatField()),
                ('lower_tunnel_price', models.FloatField()),
                ('upper_tunnel_price', models.FloatField()),
                ('percentage_change', models.FloatField()),
                ('period', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='asset_images/')),
                ('user_has_assets', models.ManyToManyField(related_name='user_assets_asset', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='assets',
            field=models.ManyToManyField(blank=True, related_name='user_assets', to='core.asset'),
        ),
    ]
