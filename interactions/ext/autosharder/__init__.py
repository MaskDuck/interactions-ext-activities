from interactions import Client
from interactions.api.models.team import Application
import interactions
from interactions.api.gateway import WebSocketClient
from interactions.api.models.flags import Intents
import asyncio
from interactions.base import get_logger

log = get_logger("client")
class AutoShardedClient(Client):
    def __init__(
        self,
        token: str,
        **kwargs,
    ) -> None:
        r"""
        Establishes a client connection to the Web API and Gateway.
        :param token: The token of the application for authentication and connection.
        :type token: str
        :param \**kwargs: Multiple key-word arguments able to be passed through.
        :type \**kwargs: dict
        """

        # Arguments
        # ~~~~~~~~~
        # token : str
        #     The token of the application for authentication and connection.
        # intents? : Optional[Intents]
        #     Allows specific control of permissions the application has when connected.
        #     In order to use multiple intents, the | operator is recommended.
        #     Defaults to ``Intents.DEFAULT``.
        # shards? : Optional[List[Tuple[int]]]
        #     Dictates and controls the shards that the application connects under.
        # presence? : Optional[ClientPresence]
        #     Sets an RPC-like presence on the application when connected to the Gateway.
        # disable_sync? : Optional[bool]
        #     Controls whether synchronization in the user-facing API should be automatic or not.

        self._loop = asyncio.get_event_loop()
        self._http = interactions.api.http.client.HTTPClient(token=token)
        self._intents = kwargs.get("intents", Intents.DEFAULT)
        self._websocket = WebSocketClient(token=token, intents=self._intents)
        self._shard = kwargs.get("shards")
        self._presence = kwargs.get("presence")
        self._token = token
        self._extensions = {}
        self._scopes = set([])
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
            self._shard = await self._http.get_gateway_bot()[0]
            print(self._shard)
        while not self._websocket._closed:
            loops = [await self._websocket._establish_connection(x, self._presence) for x in self._shard_list_generator(self._shard)]
            await asyncio.gather(*loops, loop=asyncio.get_event_loop())
