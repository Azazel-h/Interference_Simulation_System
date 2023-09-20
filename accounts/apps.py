from django.apps import AppConfig
from django.conf import settings

from misc.network.ldap_protocol import LDAPConnection


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    ldap_connections = None
    name = 'accounts'

    def ready(self):
        self.ldap_connections = (
            # Employee LDAP
            LDAPConnection(
                'Employee',
                'ldaps://mail.bmstu.ru:636',
                f'{settings.__getattr__("LDAP_USERNAME")}@bmstu.ru',
                settings.__getattr__('LDAP_PASSWORD'),
                'cn=bmstu.ru',
            ),
            # Student LDAP
            LDAPConnection(
                'Student',
                'ldaps://mailstudent.bmstu.ru:636',
                f'{settings.__getattr__("LDAP_USERNAME")}@mailstudent.bmstu.ru',
                settings.__getattr__('LDAP_PASSWORD'),
                'cn=student.bmstu.ru',
            ),
        )
