from interactions import Client
import asyncio

class AutoShardedClient(Client):
    async def _shard_list_generator(self, shard_count):
        """A helper method to generate shards."""
        if shard_count is not []:
            shard_list = [[a, shard_count] for a in range(0, shard_count)]
        return shard_list

    async def _login(self):
        if self._shard is []:
            self._shard = await self._http.get_gateway_bot()[0]
        while not self._websocket._closed:
            loops = [await self._websocket._establish_connection(x, self._presence) for x in self._shard_list_generator(self._shard)]
            await asyncio.gather(*loops, loop=asyncio.get_event_loop())
