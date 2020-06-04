import discord
import configparser
import aiohttp
import json
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from esoeventplanner.eventplanner import eventplanner
from datetime import datetime

def get_author(context):
    return str(context.author).split("#")[0]

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('bot.conf')
    token = config['DEFAULT']['token']
    servername = config['DEFAULT']['servername']

    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        print ("Bot is now ready.")

    @bot.command()
    async def create_event(ctx, *args, **kwargs):
        author = get_author(ctx)
        eventobj = eventplanner(servername)
        date, description, time, host = str(args[0]), str(args[1]), str(args[2]), str(args[3])
        eventobj.create_event(date,description,time,host,author)
        await ctx.send("{} created a new event at {} on {} doing {} hosted by {}".format(author, time, date, description, host))

    @bot.command()
    async def initalize_events(ctx):
        author = get_author(ctx)
        eventobj = eventplanner(servername)
        res = eventobj.initalize()
        await ctx.send("{} tried to initalize the event DB with a result of {}".format(author, res))

    @bot.command()
    async def get_todays_events(ctx):
        embed = discord.Embed(title="Today's Events (all times in CST)", desc="List of events today")
        eventobj = eventplanner(servername)
        mydate = datetime.now().strftime('%m/%d/%Y')
        events = eventobj.get_all_events(mydate)
        if not events:
            embed.add_field(name="No events posted today", value="Check back again tomorrow")
        else:
            for event in events:
                embed.add_field(name=event[2], value="{} is hosting this event at {}".format(event[4], event[3]))
        await ctx.send(embed=embed)

    @bot.command()
    async def author(ctx):
        await ctx.send("Dub created me, especially for TDD and TOH")

    @bot.command()
    async def whydadjoke(ctx):
        await ctx.send("Annabanana of course")

    @bot.command()
    async def dadjoke(ctx, *args):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://icanhazdadjoke.com') as request:
                if request.status == 200:
                    data = await request.text()
                    await ctx.send(data)

    @bot.command()
    async def survey(ctx, *, arg):
        map = "-".join(arg.split(" "))
        embed = discord.Embed(title="{} survey map".format(arg), desc="Requested Survey Map")
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.elderscrollsguides.com/survey-maps/{}/".format(map)) as request:
                if request.status == 200:
                    data = await request.text()
                    soup = BeautifulSoup(data, "html.parser")
                    for img in soup.find_all("img"):
                        if map in img['src'].lower():
                            embed.set_image(url="{}".format(img['src']))
                    await ctx.send(embed=embed)

    @bot.command()
    async def treasure(ctx, *, arg):
        map = "-".join(arg.split(" "))
        embed = discord.Embed(title="{} treasure map".format(arg), desc="Requested Teasure Map")
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.elderscrollsguides.com/treasure-maps/{}/".format(map)) as request:
                if request.status == 200:
                    data = await request.text()
                    soup = BeautifulSoup(data, "html.parser")
                    for img in soup.find_all("img"):
                        if map in img['src'].lower():
                            embed.set_image(url="{}".format(img['src']))
                    await ctx.send(embed=embed)
    @bot.command()
    async def skyshards(ctx, *, arg):
        map = "-".join(arg.split(" "))
        embed = discord.Embed(title="{} skyshard map".format(arg), desc="Requested Skyshard Map")
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.elderscrollsguides.com/skyshards/{}/".format(map)) as request:
                if request.status == 200:
                    data = await request.text()
                    soup = BeautifulSoup(data, "html.parser")
                    for img in soup.find_all("img"):
                        if map in img['src'].lower():
                            embed.set_image(url="{}".format(img['src']))
                    await ctx.send(embed=embed)

    bot.run(token)
