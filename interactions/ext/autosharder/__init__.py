from interactions import Client
from interactions.api.models.team import Application
import interactions
from interactions.api.gateway import WebSocketClient
from contextlib import suppress
from interactions.api.models.flags import Intents
import asyncio
from interactions.base import get_logger

log = get_logger("client")


class AutoShardedClient(Client):
    """A sharded implementation. This just exist to override the _login coroutine to create multiple websocket instance."""
    def __init__(
        self,
        token: str,
        **kwargs,
    ) -> None:
        r"""
        This is interactions.py's init but modified a bit for sharding purpose.
        """

        self._loop = asyncio.get_event_loop()
        self._http = interactions.api.http.HTTPClient(token=token)
        self._intents = kwargs.get("intents", Intents.DEFAULT)
        self._websocket = WebSocketClient(token=token, intents=self._intents)
        self._shard = kwargs.get("shards")
        self._presence = kwargs.get("presence")
        self._token = token
        self._extensions = {}  # type: ignore
        self._scopes = set([])  # type: ignore
        self.me = None
        _token = self._token  # noqa: F841
        _cache = self._http.cache  # noqa: F841

        if kwargs.get("disable_sync"):
            self._automate_sync = False
            log.warning(
                "Automatic synchronization has been disabled. Interactions may need to be manually synchronized."
            )
        else:
            self._automate_sync = True

        data = self._loop.run_until_complete(self._http.get_current_bot_information())
        self.me = Application(**data)

    def _shard_list_generator(self, shard_count):
        """A helper method to generate shards."""
        for x in range(0, shard_count):
            yield [x, shard_count]

    async def _login(self):
        if self._shard is None:
            bot_gw = await self._http.get_bot_gateway()
            self._shard = bot_gw[0]
            # print(self._shard)
        with suppress(KeyboardInterrupt):
            while not self._websocket._closed:
                loops = [
                    await self._websocket._establish_connection(x, self._presence)
                    for x in self._shard_list_generator(self._shard)
                ]
                await asyncio.gather(*loops, loop=asyncio.get_event_loop())
