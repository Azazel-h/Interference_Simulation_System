from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CASUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, uid, mail, is_staff, first_name, last_name, patronymic, title, group, departament):
        user = self.model(
            uid=uid,
            mail=self.normalize_email(mail),
            is_staff=is_staff,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            title=title,
            group=group,
            departament=departament
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, uid, mail, is_staff, first_name, last_name, patronymic, title, group, departament):
        user = self.model(
            uid=uid,
            mail=self.normalize_email(mail),
            is_staff=is_staff,
            is_superuser=True,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            title=title,
            group=group,
            departament=departament
        )
        user.save(using=self._db)

        return user


class CASUser(AbstractBaseUser, PermissionsMixin):
    password = None
    uid = models.CharField(unique=True, max_length=20)
    mail = models.EmailField(unique=True)
    is_staff = models.BooleanField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    USERNAME_FIELD = 'uid'

    objects = CASUserManager()

    def get_name(self):
        if all((self.last_name, self.first_name, self.patronymic)):
            return f'{self.last_name} {self.first_name} {self.patronymic}'
        elif all((self.last_name, self.first_name)):
            return f'{self.last_name} {self.first_name}'
        else:
            return self.uid

    def get_short_name(self):
        if all((self.last_name, self.first_name, self.patronymic)):
            return f'{self.last_name} {self.first_name[0]}. {self.patronymic[0]}.'
        elif all((self.last_name, self.first_name)):
            return f'{self.last_name} {self.first_name[0]}.'
        else:
            return self.uid
