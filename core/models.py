from django.db import models
from .validators import validate_cpf, validate_email
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail

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
    symbol = models.TextField(max_length=50)
    price = models.FloatField()
    lower_tunnel_price = models.FloatField()
    upper_tunnel_price = models.FloatField()
    percentage_change = models.FloatField()
    period = models.TextField()
    image = models.ImageField(upload_to='asset_images/', null=True, blank=True)
    user_has_assets = models.ManyToManyField(User, related_name='user_assets_asset')

    def email_tunnel_limits(self, user):
        if self.price < self.lower_tunnel_price:
            subject = f'Compra Ativo {self.symbol}.'
            message = f'Olá {user.name}, o ativo {self.symbol} ultrapassou o limite inferior de túnel, chegando ao valor {self.price}! Está na hora de comprar esse ativo.'
            send_mail(subject, message, 'eucotacoes@gmail.com', [user.email])

        elif self.price > self.upper_tunnel_price:
            subject = f'Venda  Ativo {self.symbol}.'
            message = f'Olá {user.name}, a ação {self.name} ultrapassou o limite superior de túnel, chegando ao valor {self.price}! Está na hora de comprar esse ativo.'
            send_mail(subject, message, 'eucotacoes@gmail.com', [user.email])
