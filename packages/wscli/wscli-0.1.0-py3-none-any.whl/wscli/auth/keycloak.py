from dataclasses import dataclass

from .login_tokens import LoginTokens
from .signin_details import SigninDetails
from .login import Login


@dataclass
class LoginKeyCloak(Login):

    client_id_key_cloak: str = None

    def login(details: SigninDetails):
        raise NotImplementedError

    def refresh(tokens: LoginTokens):
        raise NotImplementedError
