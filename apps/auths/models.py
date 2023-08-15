# Django
from django.db.models import (
    CharField,
    BooleanField,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

# Apps
from abstracts.validators import APIValidator
from abstracts.models import AbstractsDateTime


class CustomUserManager(
    BaseUserManager
):
    def create_user(
            self,
            login: str,
            first_name: str,
            password: str
        ) -> 'CustomUser':
        if not login:
            raise ValidationError('login required')
        try:
            user: 'CustomUser' = self.model(
                login=login,
                first_name=first_name,
                password=password
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise APIValidator(
                'Данный пользователь уже существует',
                'message',
                '400',
            )

    def create_superuser(
        self, login, first_name:str, password: str
    ) -> 'CustomUser':
        user: 'CustomUser' = self.model(
            is_staff=True,
            login=login,
            first_name=first_name,
            password=password
        )
        user.is_superuser: bool = True
        user.is_active: bool = True
        user.set_password(password)
        user.save(using=self._db)

        return user



class CustomUser(
    AbstractBaseUser,
    PermissionsMixin,
    AbstractsDateTime
):
    login = CharField(
        'Логин',
        unique=True,
        max_length=100,
        null=False
    )
    first_name = CharField(
        'Имя',
        max_length=100,
    )
    
    is_active: BooleanField = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['first_name']
    objects = CustomUserManager()

    class Meta:
        ordering = (
            'created_at',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'