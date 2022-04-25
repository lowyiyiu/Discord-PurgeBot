import discord
import time
from datetime import datetime
from discord.ext import commands
from dotenv import dotenv_values



TOKEN = dotenv_values(".env")["TOKEN"]



INTENTS = discord.Intents.default()
INTENTS.members = True

BOT = commands.Bot(command_prefix = "!!purge ", intents = INTENTS)



@BOT.event
async def on_ready():
  await BOT.change_presence(activity = discord.Game(name = "!!purge help"))

  print(f"{BOT.user.name} has connected to Discord!")

  for guild in BOT.guilds:
    print(f"{guild.name} ({guild.id})")



@BOT.command(name = "whereami", help = "Returns server and channel ID")
async def whereami(context):
  await context.message.delete(delay = 2)
  if context.guild.owner.id != context.message.author.id: return await context.send("Only the server's owner has permission to use this bot!", delete_after = 5)

  await context.send(f"Server: {context.message.guild.name} ({context.message.guild.id})\nChannel: {context.message.channel.name} ({context.message.channel.id})", delete_after = 10)



@BOT.command(name = "between", help = "Purge unpinned messages in this channel between two dates (YYYY-MM-DD)")
async def between(context, start_date = None, end_date = None, ):
  await context.message.delete(delay = 2)
  if context.guild.owner.id != context.message.author.id: return await context.send("Only the server's owner has permission to use this bot!", delete_after = 5)

  correct_usage_embed = discord.Embed(title="Usage", description = "!!purge between <start date (YYYY-MM-DD)> <end date (YYYY-MM-DD)>", color=discord.Colour.blue())

  if start_date == None or end_date == None: return await context.send(embed = correct_usage_embed, delete_after = 10)

  try:
    start_datetime  = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime    = datetime.strptime(end_date, "%Y-%m-%d")
  except:
    return await context.send(embed = correct_usage_embed, delete_after = 10)

  channel   = context.message.channel
  messages  = await channel.history(limit=500).flatten()
  queue     = [message for message in messages if not message.pinned and start_datetime <= message.created_at <= end_datetime]
  deleted   = []

  for message in queue:
    try:
      deleted.append(await message.delete())
    except:
      None
    time.sleep(1)

  await context.send(embed = discord.Embed(title = "PurgeBot [!!purge]", description = f"Successfully purged {len(deleted)} message{'s' if len(deleted) > 1 else ''}. \n Command executed by {context.author}.\n\nThis message will be deleted after 10 seconds.", color=discord.Colour.red()), delete_after = 10)



@BOT.command(name = "all", help = "Purge all unpinned messages in this channel")
async def all(context):
  await context.message.delete(delay = 2)
  if context.guild.owner.id != context.message.author.id: return await context.send("Only the server's owner has permission to use this bot!", delete_after = 5)

  deleted = await context.channel.purge(limit = 500, check = lambda message: not message.pinned, bulk = True)

  await context.send(embed = discord.Embed(title = "PurgeBot [!!purge]", description = f"Successfully purged {len(deleted)} message{'s' if len(deleted) > 1 else ''}. \n Command executed by {context.author}.\n\nThis message will be deleted after 10 seconds.", color=discord.Colour.red()), delete_after = 10)



BOT.run(TOKEN)