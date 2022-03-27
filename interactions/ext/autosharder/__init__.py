from interactions import Client, Guild

class AutoShardedClient(Client):
    def _shard_list_generator(self):
        """A helper method to generate shards."""
        if self.shard is not []:
            self._shard_list = [[a, self.shard] for a in range(1, self.shard)]
    
    async def _login(self) -> None:
        """Makes a login with the Discord API."""
        while not self._websocket._closed:
            for x in self._shard_list:
                await self._websocket._establish_connection(x, self._presence)
