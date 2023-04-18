import os

from dotenv import load_dotenv

# Carga las variables de entorno desde .env
load_dotenv()
from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent, SortMethod, TwitchAPIException

APP_ID = os.environ['TWITCH_CLIENT_ID']
APP_SECRET = os.environ['TWITCH_CLIENT_SECRET']
USER_SCOPE = [
    # leer el chat
    AuthScope.CHAT_READ,
    # escribir en el chat
    AuthScope.CHAT_EDIT,
    # mandar SO's (el usuario del bot debe ser moderador)
    AuthScope.MODERATOR_MANAGE_SHOUTOUTS,
    # leer followers (el usuario del bot debe ser moderador)
    AuthScope.MODERATOR_READ_FOLLOWERS]
TARGET_CHANNEL = os.environ['TWITCH_CHANNEL']
BOT_USERNAME = os.environ['TWITCH_USERNAME']


class TwitchConnection:
    def __init__(self):
        self._twitch = None

    @property
    async def twitch(self):
        if not self._twitch:
            print("Pillando conexión")
            await self.connect()
        return self._twitch

    async def connect(self):
        # set up twitch api instance and add user authentication with some scopes
        twitch = await Twitch(APP_ID, APP_SECRET)
        twitch.app_auth_refresh_callback = self.app_refresh
        twitch.user_auth_refresh_callback = self.user_refresh
        auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        return twitch

    async def user_refresh(token: str, refresh_token: str):
        print(f'my new user token is: {token}')

    async def app_refresh(token: str):
        print(f'my new app token is: {token}')
