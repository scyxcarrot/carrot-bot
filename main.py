import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server, {member.name}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "hello" in message.content.lower():
        await message.channel.send(f'Hello, {message.author.name}!')
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def assign_role(ctx, role: discord.Role):
    if role not in ctx.author.roles:
        await ctx.author.add_roles(role)
        await ctx.send(f'Role {role.name} has been assigned to you.')
    else:
        await ctx.send(f'You already have the role {role.name}.')

@bot.command()
async def remove_role(ctx, role: discord.Role):
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f'Role {role.name} has been removed from you.')
    else:
        await ctx.send(f'You never had the role {role.name}.')

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)