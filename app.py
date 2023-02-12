import discord
import random
import os
import sys
import subprocess
import requests
from PIL import Image, ImageFont, ImageDraw
import textwrap

def callJokeApi():
    x = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode')
    data = x.json()
    if data['type'] == 'single':
        return str(data['joke'])
    elif data['type'] == 'twopart':
        return str(data['setup'] + '\n' + data['delivery'])
        


bot = discord.Bot()
#put guild id(s) here
guilds = []

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=guilds, description = 'Basic command that greets you. Used to test uptime.')
async def hello(ctx):
    await ctx.respond(f"Hey, {ctx.author.id}!")

@bot.slash_command(guild_ids=guilds, description = 'Random number generator. Defaults to 1-10')
async def pickrandom(ctx, min = 1, max = 10):
    await ctx.respond("Your number is:" + str(random.randint(int(min), int(max))))

@bot.slash_command(guild_ids=guilds, description = 'Applies the latest changes globally.')
async def reload(ctx):
    await ctx.respond("Reloading...") 
    await subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])


@bot.slash_command(guild_ids=guilds, description = 'Says what you said! Says what you said!')
async def echo(ctx, text):
    message = text.replace("@", "@​")
    await ctx.respond(f"You said: {message}")

@bot.slash_command(guild_ids=guilds, description = "Tells a joke!")
async def joke(ctx):
    await ctx.respond(callJokeApi())

@bot.slash_command(guild_ids=guilds, description = "Shows current changelogs.")
async def changelogs(ctx):
    with open('/changelogs.txt', 'r') as f:
        data = f.read()
        await ctx.respond(data)

#broken command :[
@bot.slash_command(guild_ids=guilds, description = "Makes the silly garflid image speak (image by @willy on wasteof)")
async def garfild(ctx, text: str):
    
    font = ImageFont.truetype("font.ttf", 30)
    img = Image.open("pic.jpg")
    cx, cy = (325, 100)
    lines = textwrap.wrap(text, width=17)
    w, h = font.getsize(text)
    y_offset = (len(lines) * h)/2
    y_text = cy - (h/2) - y_offset
    for line in lines:
        w2,h2 = font.getsize(line)
        draw = ImageDraw.Draw(img)
        draw.text(y_text , cx - (w/2), line, (0, 0, 0), font=ImageFont.truetype("font.ttf", 30))
        img.save("edit.jpg")
        y_text += h2

    await ctx.respond(file=discord.File('edit.jpg'))
    



    



bot.run("BOT ID")
