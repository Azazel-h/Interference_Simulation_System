import logging
from typing import Optional

import ldap


class LDAPConnection:
    def __init__(self, name: str, server_uri: str = None, bind_dn: str = None, bind_password: str = None,
                 search_base: str = None) -> None:
        self.name = name
        self.server_uri = server_uri
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.search_base = search_base

        self.connection = None

        if all((self.server_uri, self.bind_dn, self.bind_password)):
            self.init_ldap_server()

    def init_ldap_server(self) -> None:
        logging.debug(f'Initializing {self.name} LDAP server')

        try:
            self.connection = ldap.initialize(self.server_uri)
            self.connection.simple_bind(self.bind_dn, self.bind_password)
        except (ldap.LDAPError, ldap.SERVER_DOWN) as error:
            self.connection = None
            logging.error(f'Failed to init {self.name} LDAP connection. Error: {error}')

    def search(self, username: str) -> Optional[dict]:
        if self.connection:
            return self.connection.search_s(self.search_base, ldap.SCOPE_SUBTREE, f'(uid={username})')
        else:
            logging.warning(f'{self.name} LDAP server isn\'t initialized')