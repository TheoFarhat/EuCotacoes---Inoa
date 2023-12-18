from django.core.exceptions import ValidationError
from django.db.models import Q


def validate_email(value):
    from .models import User 

    if not value:
        raise ValidationError('O campo Email é obrigatório.')

    
    if User.objects.filter(email=value).exists():
        raise ValidationError('Este email já está sendo utilizado.')

def validate_cpf(value):
    from .models import User 
    
    if not (isinstance(value, int) and 10000000000 <= value <= 99999999999):
        raise ValidationError('CPF deve ter 11 dígitos.')

    if User.objects.filter(cpf=value).exists():
        raise ValidationError('Este CPF já está sendo utilizado.')
