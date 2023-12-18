# Generated by Django 5.0 on 2023-12-18 04:08

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id_asset', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=50)),
                ('price', models.FloatField()),
                ('price_tunel', models.FloatField()),
                ('period', models.TextField()),
            ],
        ),
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
                ('assets', models.ManyToManyField(blank=True, related_name='user_assets', to='core.asset')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
