import aiohttp, requests
from datetime import datetime
from dateutil import parser
from cardboard.Exceptions import *
import concurrent.futures  # threading HEHE


import aiohttp


async def _handle_error(response):
    """
    Handles the error responses from API requests.

    Args:
        response (aiohttp.ClientResponse): The response object from the API request.

    Raises:
        Forbidden: If the response status code is 403.
        Unauthorized: If the response status code is 401.
        NotFound: If the response status code is 404.
        InternalServerError: If the response status code is 500.
        RateLimited: If the response status code is 429.
        CardboardException: If the response status code does not match any defined error codes.
    """
    if response.status == 403:
        raise Forbidden(await response.text())
    elif response.status == 401:
        raise Unauthorized(await response.text())
    elif response.status == 404:
        raise NotFound(await response.text())
    elif response.status == 500:
        raise InternalServerError(await response.text())
    elif response.status == 429:
        raise RateLimited(await response.text())
    elif response.status == 400:
        raise BadRequest(await response.text())
    elif 200 <= response.status < 300:
        return False
    else:
        raise CardboardException(await response.text())


class CardboardAsync:
    """
    Base asynchronous Cardboard class for interacting with the Cardboard API.

    Args:
        client_id (str): Your app's id.

        secret (str): Your app's secret.
    """

    def __init__(self, client_id: str, secret: str):
        self.client_id = client_id
        self._baseurl: str = "https://cardboard.ink/api/v1"
        self.secret: str = secret
        self.app_name: str = None
        self._session = None

        def __check_verify(self) -> bool | list:
            """
            Verifies authentication data. ID and Secret.

            Returns:
                bool|list: [True, app_name, app_vanity] if everything is valid, else False.
            """
            resp = requests.post(
                self._baseurl + "/check",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"client_id": self.client_id, "client_secret": self.secret},
            )
            if resp.status_code != 200:
                return False
            return [True, resp.json()["name"], resp.json()["vanity"]]

        self.__check_verify = lambda: __check_verify(self)
        self._valid = (
            concurrent.futures.ThreadPoolExecutor()
            .submit(lambda: self.__check_verify())
            .result()
        )
        if self._valid is False:
            raise CardboardException(
                "Invalid credentials provided. (Is your ID and Secret correct?)"
            )
        self.app_name = self._valid[1]
        self.app_url = f"https://cardboard.ink/a/{self._valid[2]}"

    class UserAlias:
        """
        UserAlias object.

        Represents a user's alias.

        Attributes:
            alias (str|None): The user's alias.
            discriminator (str|None): The user's discriminator.
            name (str): The user's name.
            createdAt (datetime.datetime): When this alias was created.
            _raw_createdAt (str): When this alias was created as an ISO formatted string.
            editedAt (datetime.datetime): When this alias was last updated. (Can be the same time as createdAt)
            _raw_editedAt (str): When this alias was last updated as an ISO formatted string. (Can be the same time as createdAt)
            userId (str): The user's ID.
            gameId (int): The game's ID.
            socialLinkSource (str|None): The social link source for the alias. This is not a URL.
            additionalInfo (dict): Additional info about this alias. This can be an empty dict.
            socialLinkHandle (str|None): The social link to the user for this alias. This is not a URL.
            playerInfo (dict|None): Player info for this alias.
            _raw (dict): Raw alias data directly from the API.
        """

        def __init__(self, data):
            self.alias: str | None = data["alias"]
            self.discriminator: str | None = data["discriminator"]
            self.name: str = data["name"]
            self.createdAt: datetime = parser.isoparse(data["createdAt"])
            self._raw_createdAt: str = data["createdAt"]
            self.editedAt: datetime = parser.isoparse(data["editedAt"])
            self._raw_editedAt: str = data["editedAt"]
            self.userId: str = data["userId"]
            self.gameId: int = data["gameId"]
            self.socialLinkSource: str | None = data["socialLinkSource"]
            self.additionalInfo: dict = data["additionalInfo"]
            self.socialLinkHandle: str | None = data["socialLinkHandle"]
            self.playerInfo: dict | None = data["playerInfo"]
            self._raw: dict = data

    class UserAbout:
        """
        UserAbout object.

        Attributes:
            bio (str|None): The user's bio.
            tagline (str|None): The user's tagLine.
            _raw (dict): The raw API data.
        """

        def __init__(self, data):
            if data:
                self.bio: str | None = data.get("bio")
                self.tagline: str | None = data.get("tagLine")
                self._raw: dict = data
            else:
                self.bio: str | None = None
                self.tagline: str | None = None
                self._raw: dict = {}

    class UserStatus:
        """
        UserStatus object.

        Attributes:
            text (str|None): The user's status text.
            reaction_id (int|None): The associated emoji with the user's stauts.
            _raw_text (dict|None): The raw API data for text. WARNING: This is highly different from this class.
            _raw_reaction (dict|None): The raw API data for the reaction. WARNING: This is highly different from this class.
            _raw (dict): The raw API data. WARNING: This is highly different from this class.
        """

        def __init__(self, data):
            try:
                self.text: str | None = data["content"]["document"]["nodes"][0][
                    "nodes"
                ][0]["leaves"][0]["text"]
            except:
                self.text: str | None = None
            self._raw_text: dict | None = data.get("content")
            self.reaction_id: int | None = data.get("customReactionId")
            self._raw: dict = data
            self._raw_reaction: dict | None = data.get("customReaction")

    class User:
        """
        User object.

        Attributes:
            name (str): The user's username.
            id (str): The user's ID.
            subdomain (str|None): The user's subdomain if available.
            aliases (list[UserAlias]): A list of user aliases.
            avatar (str): The link to the user's avatar.
            banner (str): The link to the user's banner.
            status (UserStatus): The user's status.
            moderationStatus (str|None): The user's current moderation status on Guilded.
            aboutInfo (UserAbout): The user's info, including bio and tagline.
            userTransientStatus (str|None): The user's current transient status if applicable.
            _raw (dict): The raw data returned from the API.
        """

        def __init__(self, data):
            self.name: str = data["name"]
            self.id: str = data["id"]
            self.subdomain: str | None = data.get("subdomain")
            self.aliases: list = [
                CardboardAsync.UserAlias(data) for data in data["aliases"]
            ]
            self.avatar: str = data["avatar"]
            self.banner: str = data["banner"]
            self.status: CardboardAsync.UserStatus = CardboardAsync.UserStatus(
                data["userStatus"]
            )
            self.moderationStatus: str | None = data["moderationStatus"]
            self.aboutInfo: CardboardAsync.UserAbout = CardboardAsync.UserAbout(
                data["aboutInfo"]
            )
            self.userTransientStatus: str | None = data["userTransientStatus"]
            self._raw: dict = data

    class AuthToken:
        """
        AuthToken object.

        Attributes:
            token (str): Your new authorization token.
            refresh_token (str): Your refresh token to get a new authorization token.
            token_type (str): Always "Bearer"
            expires_in (int): How many seconds your new token will last.
            _raw (dict): The raw response from the API.
        """

        def __init__(self, data):
            self.token: str = data["access_token"]
            self.refresh_token: str = data["refresh_token"]
            self.token_type: str = data["token_type"]
            self.expires_in: int = data["expires_in"]
            self._raw: dict = data

    async def _async_session_request_post_(self, url, data=None, headers=None):
        """
        Makes a post request.
        """
        if not self._session:
            self._session = aiohttp.ClientSession(
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if not headers:
            async with self._session.post(url, data=data) as response:
                resp = response
                await resp.read()
            return resp
        else:
            async with self._session.post(url, data=data, headers=headers) as response:
                resp = response
                await resp.read()
            return resp

    async def _async_session_request_get_(self, url, data=None, headers=None):
        """
        Makes a get request.
        """
        if not self._session:
            self._session = aiohttp.ClientSession(
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if not headers:
            async with self._session.get(url, data=data) as response:
                resp = response
                await resp.read()
            return resp
        else:
            async with self._session.get(url, data=data, headers=headers) as response:
                resp = response
                await resp.read()
            return resp

    async def get_token(self, code: str, client_id: str = None, secret: str = None) -> AuthToken:
        """
        Exchanges your initial code for an authorization token.

        Args:
            code(str): Your initial code.
            client_id (str|None): Your client id associated with your code. Defaults to the client id provided when you initialized this class.
            secret (str|None): Your secret associated with your code. Defaults to the secret provided when you initalized this class.
        """
        grant_type = "authorization_code"
        data = {
            "code": code,
            "client_id": client_id if client_id else self.client_id,
            "client_secret": secret if secret else self.secret,
            "grant_type": grant_type,
        }
        response = await self._async_session_request_post_(
            f"{self._baseurl}/token", data=data
        )
        if response.status != 200:
            await _handle_error(response)
        return self.AuthToken(await response.json())

    async def refresh_token(self, refresh_token: str, client_id: str = None, secret: str = None) -> AuthToken:
        """
        Refreshes your authorization token. Your old authorization token and refresh token will no longer work after this.

        Args:
            refresh_token (str): Your refresh token.
            client_id (str|None): Your client id associated with your refresh token. Defaults to the client id provided when you initialized this class.
            secret (str|None): Your secret associated with your refresh token. Defaults to the secret provided when you initalized this class.
        """
        grant_type = "refresh_token"
        data = {
            "refresh_token": refresh_token,
            "client_id": client_id if client_id else self.client_id,
            "client_secret": secret if secret else self.secret,
            "grant_type": grant_type,
        }
        response = await self._async_session_request_post_(
            f"{self._baseurl}/token", data=data
        )
        if response.status != 200:
            await _handle_error(response)
        return self.AuthToken(await response.json())

    async def revoke_token(self, token: str, client_id: str = None, secret: str = None) -> None:
        """
        Revokes an authorization token. This also revokes your refresh token associated with this authorization token.

        Args:
            token (str): Your authorization token.
            client_id (str|None): Your client id associated with your authorization token. Defaults to the client id provided when you initialized this class.
            secret (str|None): Your secret associated with your authorization token. Defaults to the secret provided when you initalized this class.
        """
        data = {
            "client_id": client_id if client_id else self.client_id,
            "client_secret": secret if secret else self.secret,
            "token": token,
        }
        response = await self._async_session_request_post_(
            f"{self._baseurl}/token/revoke", data=data
        )
        if response.status != 200:
            await _handle_error(response)

    async def get_user(self, token: str) -> User:
        """
        Fetches user data.

        Args:
            token (str): Your authorization token.
        """
        headers = {"Authorization": f"Bearer {token}"}
        response = await self._async_session_request_get_(
            f"{self._baseurl}/users/@me", headers=headers
        )
        if response.status != 200:
            await _handle_error(response)
        return self.User(await response.json())

    async def check_token(self, token: str, client_id: str = None, secret: str = None) -> bool:
        """
        Checks whether a token is valid or not.

        Args:
            token (str): Your authorization token.
            client_id (str|None): Your client id associated with your authorization token. Defaults to the client id provided when you initialized this class.
            secret (str|None): Your secret associated with your authorization token. Defaults to the secret provided when you initalized this class.
        """
        data = {
            "token": token,
            "client_id": client_id if client_id else self.client_id,
            "client_secret": secret if secret else self.secret,
        }
        response = await self._async_session_request_post_(
            f"{self._baseurl}/token/check", data=data
        )
        if response.status != 200:
            await _handle_error(response)
        return (await response.json())["validity"]
