import logging
from typing import Optional

from django.conf import settings
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

        username = self.clean_username(username)
        user_model = get_user_model()
        user_ldap_info = None
        is_staff = True

        for ln in ('EMPLOYEE', 'STUDENT'):
            ldap_con = settings.__getattr__(f'{ln}_LDAP')

            if user_ldap_info is None:
                logging.debug(f'Searching in {ldap_con.name} server')
                data = ldap_con.search(username)

                if data:
                    user_ldap_info = data[0][1]
                    user_ldap_info['is_staff'] = is_staff

                is_staff = False

        if user_ldap_info is None:
            return None

        full_name = user_ldap_info['cn'][0].decode().split()
        user_kwargs = {
            'uid': user_ldap_info['uid'][0].decode(),
            'mail': user_ldap_info['mail'][0].decode(),
            'is_staff': user_ldap_info['is_staff'],
            'first_name': full_name[1],
            'last_name': full_name[0],
            'patronymic': full_name[2] if len(full_name) == 3 else '',
            'title': user_ldap_info['ou'][0].decode(),
        }

        user, created = user_model._default_manager.update_or_create(uid=username, defaults=user_kwargs)

        if created:
            user = self.configure_user(user)

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
