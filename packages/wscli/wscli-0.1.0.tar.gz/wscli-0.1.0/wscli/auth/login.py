from typing import Protocol

from .signin_details import SigninDetails
from .login_tokens import LoginTokens


class Login(Protocol):
    def login(details: SigninDetails) -> LoginTokens: ...
    def refresh(tokens: LoginTokens) -> LoginTokens: ...
