import logging
from interactions.ext.autosharder import AutoShardedClient

bot = AutoShardedClient(token="token_here", disable_sync=False, shards=69)  # Note: if you don't provide shards then it will adjust to the recommended amount for your bot.

@bot.event
async def on_ready():
    print("bot is now online.")

@bot.command(name="intent", description="h")
async def intent(ctx):
    await ctx.send("hola")

bot.start()