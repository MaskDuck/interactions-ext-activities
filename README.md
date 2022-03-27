# interactions-ext-autosharder
Imagine when your bot is too large and Discord ask you to sharding and you dont really know how to shard but i.py doesn't have automatic sharding support :trollface:

Your problem is now solved by this wrapper!

# Examples
```python
from interactions.ext.autosharder import AutoShardedClient

bot = AutoShardedClient(token="token_here", disable_sync=False, shards=69)  # SEE NOTE

@bot.event
async def on_ready():
    print("bot is now online.")

@bot.command(name="intent", description="h")
async def intent(ctx):
    await ctx.send("hola")

bot.start()
```
Note: I would recommend you to omit the `shards` kwarg. If you omit the `shards` kwarg, it would adjust to the best number of shards for your bot.


# Installation

`pip install git+https://github.com/MaskDuck/interactions-ext-autosharder`


# Warning: This script is in beta and may have bugs. Use at your own risk.
