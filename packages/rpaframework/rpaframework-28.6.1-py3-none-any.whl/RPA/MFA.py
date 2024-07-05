import logging
from enum import Enum
from typing import List, Optional

from pyotp import HOTP, TOTP
from requests_oauthlib import OAuth2Session
from robot.api.deco import keyword

from RPA.Robocorp.Vault import Vault
from RPA.Robocorp.utils import protect_keywords


class OTPMode(Enum):
    """Enumeration for type of OTP to use."""

    TIME = "TIME"
    COUNTER = "COUNTER"


class TOTPNotSetError(Exception):
    """Raised when TOTP (Time-based One-Time Password) has not been set."""

    ERROR_MSG = (
        "TOTP (Time-based One-Time Password) can be set during the library "
        "initialization. With `Use MFA Secret From Vault` keyword or with "
        "`Set Time Based OTP` keyword."
    )


class HOTPNotSetError(Exception):
    """Raised when HOTP (HMAC One-Time Password) has not been set."""

    ERROR_MSG = (
        "HOTP (HMAC One-Time Password) can be set during the library "
        "initialization. With `Use MFA Secret From Vault` keyword or with "
        "`Set Counter Based OTP` keyword."
    )


class OAuth2NotSetError(Exception):
    """Raised when OAuth2 session object isn't initialized but used."""

    ERROR_MSG = (
        "OAuth2 session required but not initialized, please call the "
        "`Generate OAuth URL` keyword first."
    )


class MFA:
    """**RPA.MFA** is a library intended mainly for generating one-time passwords (OTP)
    and not only, as OAuth2 support was introduced lately.

    Library requires at the minimum `rpaframework` version **19.4.0**.

    Based on the `pyotp <https://pypi.org/project/pyotp/>`_ and
    `requests_oauthlib <https://pypi.org/project/requests-oauthlib/>`_ packages. It
    provides support for both MFA with the ``* OTP`` related keywords and OAuth2
    "Authorization Code Flow" with the ``* OAuth *`` related keywords.

    In the below example the **mfa** secret we are reading from the Robocorp
    Vault is the passcode generated by the Authenticator service. The passcode
    value is stored into the Vault with key **otpsecret**.

    Passcode is typically a long string (16-32 characters), which is provided
    in a form of QR image, but it can be obtained by requesting access to a string.

    Note that same code can be used to add a mobile phone as a duplicate authentication
    device at the same time when the same code is added into the Vault.

    **Robot framework example usage:**

    .. code-block:: robotframework

        *** Settings ***
        Library     RPA.MFA
        Library     RPA.Robocorp.Vault

        *** Tasks ***
        Generate time based code
            ${secrets}=    Get Secret   mfa
            ${code}=    Get Time Based OTP    ${secrets}[otpsecret]


    **Python example usage**

    .. code-block:: python

        from RPA.MFA import MFA
        from RPA.Robocorp.Vault import Vault


        def main():
            secrets = Vault().get_secret("mfa")
            code = MFA().get_time_based_otp(secrets["otpsecret"])
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "REST"

    def __init__(
        self,
        vault_name: Optional[str] = None,
        vault_key: Optional[str] = None,
        mode: Optional[OTPMode] = OTPMode.TIME,
    ):
        protect_keywords("RPA.MFA", ["get_oauth_token", "refresh_oauth_token"])
        self.logger = logging.getLogger(__name__)

        self._hotp: Optional[HOTP] = None
        self._totp: Optional[TOTP] = None
        if vault_name and vault_key:
            self.use_mfa_secret_from_vault(vault_name, vault_key, mode)
        self._oauth: Optional[OAuth2Session] = None

    @keyword
    def use_mfa_secret_from_vault(
        self, vault_name: str, vault_key: str, mode: OTPMode = OTPMode.TIME
    ):
        """Set `time` or `counter` based OTP with passcode stored in
        the Robocorp Vault named with `vault_name` under key of `vault_key`.

        :param vault_name: name of the vault storing the passcode
        :param vault_key: name of the vault key storing the passcode value
        """
        secrets = Vault().get_secret(vault_name)
        if mode == OTPMode.TIME:
            self.set_time_based_otp(secrets[vault_key])
        elif mode == OTPMode.COUNTER:
            self.set_counter_based_otp(secrets[vault_key])

    @keyword
    def set_time_based_otp(self, otp_passcode: str):
        """Set `time` based OTP with passcode.

        :param otp_passcode: the passcode provided by the Authenticator
        """
        self._totp = TOTP(otp_passcode)

    @keyword
    def set_counter_based_otp(self, otp_passcode: str):
        """Set `counter` based OTP with passcode.

        :param otp_passcode: the passcode provided by the Authenticator
        """
        self._hotp = HOTP(otp_passcode)

    @keyword
    def get_time_based_otp(self, otp_passcode: Optional[str] = None):
        """Get `time` based one time password using separately set
        passcode or by parameter `otp_passcode`.

        :param otp_passcode: the passcode provided by the Authenticator
        """
        if otp_passcode:
            self.set_time_based_otp(otp_passcode)
        if not self._totp:
            raise TOTPNotSetError(TOTPNotSetError.ERROR_MSG)
        return self._totp.now()

    @keyword
    def get_counter_based_otp(
        self,
        counter: int,
        otp_passcode: Optional[str] = None,
    ):
        """Get `counter` based one time password using separately set
        passcode or by parameter `otp_passcode`. The counter index is
        given by the `counter` parameter.

        :param counter: the index of the counter
        :param otp_passcode: the passcode provided by the Authenticator
        """
        if otp_passcode:
            self.set_counter_based_otp(otp_passcode)
        if not self._hotp:
            raise HOTPNotSetError(HOTPNotSetError.ERROR_MSG)
        return self._hotp.at(counter)

    @property
    def oauth(self) -> OAuth2Session:
        """Raises if there's no OAuth2 session already created."""
        if not self._oauth:
            raise OAuth2NotSetError(OAuth2NotSetError.ERROR_MSG)

        return self._oauth

    @keyword
    def generate_oauth_url(
        self, auth_url: str, *, client_id: str, redirect_uri: str, scope: str, **kwargs
    ) -> str:
        """Generates an authorization URL which must be opened by the user to start the
        OAuth2 flow and obtain an authorization code as response.

        The received response URL should be passed further with ``Get OAuth Token`` in
        order to complete the flow. Arbitrary keyword arguments can be passed to the
        keyword, which will be redirected to the wrapped `oauthlib` library method
        call.

        :param auth_url: Authorization endpoint to call the request on. (https URL
            usually ending with '/authorize')
        :param client_id: Client app ID. (generated by the provider)
        :param redirect_uri: Redirect URL allowed by the Client app configuration. (
            necessary for getting the `code` response)
        :param scope: Space-separated string of permissions. (accepted during the
            consent screen)
        :returns: Authorization URL string not containing any sensitive info in it.
            (call it with `access_type="offline"` or set the right `scope` in the
            authorization URL for ensuring the existence of the refresh token)

        **Example: Robot Framework**

        .. code-block:: robotframework

            *** Tasks ***
            Start OAuth Flow
                ${auth_url} =    Generate OAuth URL
                ...     https://accounts.google.com/o/oauth2/auth
                ...     client_id=810482312368-19htmcgcj*******googleusercontent.com
                ...     redirect_uri=https://developers.google.com/oauthplayground
                ...     scope=https://mail.google.com
                ...     access_type=offline     prompt=consent  # explicit grant
                Log     Start OAuth2 flow: ${auth_url}

        **Example: Python**

        .. code-block:: python

            from RPA.MFA import MFA

            lib_mfa = MFA()
            auth_url = lib_mfa.generate_oauth_url(
                "https://accounts.google.com/o/oauth2/auth", ...
            )
            print(f"Start OAuth2 flow: {auth_url}")
        """
        scopes: List[str] = scope.split()
        self._oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
        authorization_url, _ = self.oauth.authorization_url(auth_url, **kwargs)
        return authorization_url

    @keyword
    def get_oauth_token(
        self, token_url: str, *, client_secret: str, response_url: str, **kwargs
    ) -> dict:
        """Exchanges the code obtained previously with ``Generate OAuth URL`` for a
        token.

        The refresh token from the returned dictionary can be used further with the
        ``Refresh OAuth Token`` keyword in order to obtain a new access token when the
        previous one expires. (usually after one hour)
        Arbitrary keyword arguments can be passed to the keyword, which will be
        redirected to the wrapped `oauthlib` library method call.

        :param token_url: Token endpoint used with a POST request in order to retrieve
            the token data. (https URL usually ending with '/token')
        :param client_secret: Client app secret. (generated by the provider)
        :param response_url: The final URL containing the authorization `code` found in
            the address bar after authenticating and authorizing the Client app
            through the authorization URL.
        :returns: A dictionary containing the access token, metadata and optionally the
            refresh token.

        **Example: Robot Framework**

        .. code-block:: robotframework

            *** Tasks ***
            Finish OAuth Flow
                ${token} =      Get OAuth Token
                ...     https://accounts.google.com/o/oauth2/token
                ...     client_secret=GOCSPX-******mqZAW89
                ...     response_url=${resp_url}  # redirect of `Generate OAuth URL`

        **Example: Python**

        .. code-block:: python

            from RPA.MFA import MFA

            lib_mfa = MFA()
            lib_mfa.get_oauth_token("https://accounts.google.com/o/oauth2/token", ...)
        """
        token = self.oauth.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=response_url,
            **kwargs,
        )
        return dict(token)

    @keyword
    def refresh_oauth_token(
        self,
        token_url: str,
        *,
        client_id: Optional[str] = None,
        client_secret: str,
        refresh_token: Optional[str] = None,
        **kwargs,
    ) -> dict:
        """Refreshes the token as the access one usually expires after 1h and the
        refresh one never expires. (as long as it doesn't get revoked)

        The effect of this keyword is similar to ``Get OAuth Token``, but this time you
        refresh unattended an already existing token by receiving a new one instead.
        Arbitrary keyword arguments can be passed to the keyword, which will be
        redirected to the wrapped `oauthlib` library method call.

        :param token_url: Token endpoint used with a POST request in order to refresh
            the token data. (https URL usually ending with '/token')
        :param client_id: Client app ID. (generated by the provider)
        :param client_secret: Client app secret. (generated by the provider)
        :param refresh_token: Refresh token string found in the dictionary obtained
            with ``Get OAuth Token`` or ``Refresh OAuth Token``.
        :returns: A token dictionary containing a new access token and updated
            metadata. (the refresh token inside isn't guaranteed to remain constant)

        **Example: Robot Framework**

        .. code-block:: robotframework

            *** Tasks ***
            Refresh OAuth Flow
                ${token} =      Refresh OAuth Token
                ...     https://accounts.google.com/o/oauth2/token
                ...     client_id=810482312368-19htmcgcj*******googleusercontent.com
                ...     client_secret=GOCSPX-******mqZAW89
                ...     refresh_token=${token}[refresh_token]  # from `Get OAuth Token`

        **Example: Python**

        .. code-block:: python

            from RPA.MFA import MFA

            lib_mfa = MFA()
            lib_mfa.refresh_oauth_token(
                "https://accounts.google.com/o/oauth2/token", ...
            )
        """
        self._oauth = self._oauth or OAuth2Session(client_id)
        token = self.oauth.refresh_token(
            token_url,
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            **kwargs,
        )
        return dict(token)
