import discord
from discord.ext import commands
import requests
import random

# Replace 'your_token_here' with your actual bot token
TOKEN = ''
PINTEREST_ACCESS_TOKEN = ''
# Create an instance of Intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Create a new bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

# Example command
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command(name='searchpin')
async def search_pin(ctx, *, keyword):
    headers = {
        "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "query": keyword,
        "fields": "id,image,link"
    }
    response = requests.get('https://api.pinterest.com/v5/search/pins', headers=headers, params=params)

    if response.status_code == 200:
        pins = response.json().get('data', [])
        if pins:
            random_pin = random.choice(pins)
            image_url = random_pin['image']['original']['url']
            pin_link = random_pin['link']
            await ctx.send(f"Here's a pin related to '{keyword}':")
            await ctx.send(image_url)
            await ctx.send(pin_link)
        else:
            await ctx.send(f"No pins found related to '{keyword}'.")
    else:
        await ctx.send("Failed to search pins on Pinterest.")
        await ctx.send(f"Status Code: {response.status_code}")
        await ctx.send(f"Response Content: {response.content}")

# Run the bot
bot.run(TOKEN)