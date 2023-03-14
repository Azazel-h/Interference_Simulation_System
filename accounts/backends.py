import logging
from typing import Optional

import ldap
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

        if settings.CAS_USERNAME_ATTRIBUTE != 'cas:user' and settings.CAS_VERSION != 'CAS_2_SAML_1_0':
            if attributes:
                username = attributes.get(settings.CAS_USERNAME_ATTRIBUTE)
            else:
                return None

        if not username:
            return None

        username = self.clean_username(username)

        if attributes:
            reject = self.bad_attributes_reject(request, username, attributes)
            if reject:
                return None

            for cas_attr_name, req_attr_name in settings.CAS_RENAME_ATTRIBUTES.items():
                if cas_attr_name in attributes and cas_attr_name is not req_attr_name:
                    attributes[req_attr_name] = attributes[cas_attr_name]
                    attributes.pop(cas_attr_name)

        user_model = get_user_model()
        user_ldap_info = None
        is_staff = True

        for ls in ('EMPLOYEE', 'STUDENT'):
            if user_ldap_info is None:
                logging.debug(f'Searching in {ls} server')

                try:
                    l = ldap.initialize(settings.__getattr__(f'{ls}_LDAP_SERVER_URI'))
                    l.simple_bind(settings.__getattr__(f'{ls}_LDAP_BIND_DN'), settings.__getattr__(f'{ls}_LDAP_BIND_PASSWORD'))
                    data = l.search_s(settings.__getattr__(f'{ls}_LDAP_BASE'), ldap.SCOPE_SUBTREE, f'(uid={username})')

                    if data:
                        user_ldap_info = data[0][1]
                    else:
                        is_staff = False
                except ldap.LDAPError as error:
                    logging.warning(f'LDAP error: {error}')

        if user_ldap_info is None:
            return None

        full_name = user_ldap_info['cn'][0].decode().split()
        user_kwargs = {
            'uid': user_ldap_info['uid'][0].decode(),
            'mail': user_ldap_info['mail'][0].decode(),
            'is_staff': is_staff,
            'first_name': full_name[1],
            'last_name': full_name[0],
            'patronymic': full_name[2] if len(full_name) == 3 else '',
            'title': user_ldap_info['ou'][0].decode(),
        }

        if settings.CAS_CREATE_USER_WITH_ID:
            user_kwargs['id'] = self.get_user_id(attributes)

        user, created = user_model._default_manager.get_or_create(**user_kwargs)
        if created:
            user = self.configure_user(user)

        if not self.user_can_authenticate(user):
            return None

        if pgtiou and settings.CAS_PROXY_CALLBACK and request:
            request.session['pgtiou'] = pgtiou

        if settings.CAS_APPLY_ATTRIBUTES_TO_USER and attributes:
            user_model_fields = user_model._meta.fields
            for field in user_model_fields:
                if not field.null:
                    try:
                        if attributes[field.name] is None:
                            attributes[field.name] = ''
                    except KeyError:
                        continue
                if field.get_internal_type() == 'BooleanField':
                    try:
                        boolean_value = attributes[field.name] == 'True'
                        attributes[field.name] = boolean_value
                    except KeyError:
                        continue

            user.__dict__.update(attributes)

            if settings.CAS_CREATE_USER:
                user.save()

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
