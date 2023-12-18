from django.db import models
from .validators import validate_cpf, validate_email
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Coloque o email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id_user = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    age = models.IntegerField()
    cpf = models.IntegerField(unique=True, validators=[validate_cpf])
    email = models.EmailField(unique=True, validators=[validate_email])
    assets = models.ManyToManyField('Asset', related_name='user_assets', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'age', 'cpf'] 

    def __str__(self):
        return self.email

class Asset(models.Model):
    id_asset = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    price = models.FloatField()
    price_tunel = models.FloatField()
    period = models.TextField()
