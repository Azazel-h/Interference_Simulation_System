import logging
from typing import Optional

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpRequest
from django_cas_ng.backends import CASBackend
from django_cas_ng.signals import cas_user_authenticated
from django_cas_ng.utils import get_cas_client


class AuthBackend(CASBackend):
    def authenticate(self, request: HttpRequest, ticket: str, service: str) -> Optional[User]:
        client = get_cas_client(service_url=service, request=request)
        username, attributes, pgtiou = client.verify_ticket(ticket)

        if attributes and request:
            request.session['attributes'] = attributes

        if not username:
            return None

        # CASUser model from `accounts` models.py:
        # Columns:
        #   id - user id (integer (auto increment))
        #   last_login - last login datetime (datetime)
        #   is_superuser - is user a superuser? (bool)
        #   uid - uid in BMSTU network (unique string (20 symbols))
        #   mail - email in BMSTU network (unique string (254 symbols))
        #   is_staff - is user a staff of BMSTU? (bool)
        #   first_name - first name (string (100 symbols))
        #   last_name - last name (string (100 symbols))
        #   patronymic - patronymic (string (100 symbols))
        #   title - department for students, job title for staff (string (100 symbols))
        user_model = get_user_model()

        username = self.clean_username(username)
        user_ldap_info = None
        is_staff = True

        ldap_conns = apps.get_app_config('accounts').ldap_connections

        if ldap_conns:
            for ldap_conn in ldap_conns:
                if user_ldap_info is None:
                    logging.debug(f'Searching in {ldap_conn.name} server')
                    data = ldap_conn.search(username)

                    if data:
                        user_ldap_info = data[0][1]
                        user_ldap_info['is_staff'] = is_staff

                    is_staff = False

        user_kwargs = {
            'uid': username,
            'is_staff': False,
        }

        if user_ldap_info:
            full_name = user_ldap_info['cn'][0].decode().split()

            user_kwargs['mail'] = user_ldap_info['mail'][0].decode()
            user_kwargs['is_staff'] = user_ldap_info['is_staff']
            user_kwargs['first_name'] = full_name[1]
            user_kwargs['last_name'] = full_name[0]
            user_kwargs['patronymic'] = full_name[2] if len(full_name) == 3 else ''
            user_kwargs['title'] = user_ldap_info['ou'][0].decode()

            is_update = True
        else:
            is_update = False

        user = user_model._default_manager.filter(uid=username).first()

        if user:
            if is_update:
                for (key, value) in user_kwargs.items():
                    setattr(user, key, value)
                user.save()
            created = False
        else:
            user = self.configure_user(user_model._default_manager.create(**user_kwargs))
            created = True

        if not self.user_can_authenticate(user):
            return None

        cas_user_authenticated.send(
            sender=self,
            user=user,
            created=created,
            username=username,
            attributes=attributes,
            pgtiou=pgtiou,
            ticket=ticket,
            service=service,
            request=request
        )

        return user
