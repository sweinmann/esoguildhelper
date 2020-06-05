import discord
import configparser
import aiohttp
import json
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from esoeventplanner.eventplanner import eventplanner
from datetime import datetime
import random
from giphy.giphy import giphy

def get_author(context):
    return str(context.author).split("#")[0]

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('bot.conf')
    token = config['DEFAULT']['token']
    servername = config['DEFAULT']['servername']
    giphyinv = config['DEFAULT']['giphyinv']

    bot = commands.Bot(command_prefix='!')
    bot.remove_command("price")
    bot.remove_command("help")

    #Create a new giphy object here
    giphyobj = giphy(giphyinv)

    @bot.event
    async def on_ready():
        print ("------------------------------------")
        print ("Bot Name: " + bot.user.name)
        print ("Bot ID: {}".format(str(bot.user.id)))
        print ("Discord Version: {}".format (discord.__version__))
        print ("------------------------------------")

    @bot.command()
    async def spank(ctx, member):
        intros = ["Brown Chicken, Brown Cow!!", "Oh my!!", "That's Hot!!", "Thats not nice, or is it??", "It's about time!!"
                  "Hon hon hon!!", "Is that all you got?", "Did you hear that?", "It's about to go down!!"]
        await ctx.send ("{} {} spanked {}".format(random.choice(intros),ctx.author.mention,member))

    @bot.command()
    async def help(ctx):
        author = ctx.message.author

        embed = discord.Embed(
            colour = discord.Colour.orange()

        )

        embed.set_author(name="Help")
        embed.add_field(name='!create_event', value='This will create a new event. {args:[date, description, time, host] -- example: !create_event "06/10/2020" "Delves in Stormhaven" "7PM" "Dub"}', inline=False)
        embed.add_field(name='!get_todays_events', value='This will list all the events for today', inline=False)
        embed.add_field(name='!survey', value='This will pull up the survey map for a zone. {arg:[zone] -- example !survey Elsweyr}', inline=False)
        embed.add_field(name='!treasure', value='This will pull up the treasure map for for a zone. {arg:[zone] -- example !treasure craglorn}', inline=False)
        embed.add_field(name='!skyshards', value='This will pull up a skyshard map for a zone. {arg:[zone -- example !skyshards shadowfen]}', inline=False)

        await author.send(author, embed=embed)

    @bot.command()
    @commands.has_role("Master Chef")
    @commands.has_role("Sous Chef")
    @commands.has_role("Sweet Roll")
    async def create_event(ctx, *args, **kwargs):
        author = get_author(ctx)
        eventobj = eventplanner(servername)
        date, description, time, host = str(args[0]), str(args[1]), str(args[2]), str(args[3])
        eventobj.create_event(date,description,time,host,author)
        await ctx.send("{} created a new event at {} on {} doing {} hosted by {}".format(author, time, date, description, host))

    @bot.command()
    @commands.has_role("Master Chef")
    @commands.has_role("Sous Chef")
    @commands.has_role("Sweet Roll")
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
    '''
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
    '''

    @bot.command()
    async def survey(ctx, *, arg):
        map = "-".join(arg.split(" ")).lower()
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
        map = "-".join(arg.split(" ")).lower()
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
        map = "-".join(arg.split(" ")).lower()
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

    @bot.command()
    async def add_giphy(ctx, name, url):
        giphyobj.add_giphy(name, url)
        await ctx.send("{} added a new giphy named {}".format(ctx.author.mention, name))

    @bot.command()
    async def get_giphy(ctx, name):
        giphyimg = giphyobj.get_giphy(name)
        embed = discord.Embed(title="Giphy Image {}".format(name), desc="Enjoy you giphy image")
        embed.set_image(url="{}".format(giphyimg))
        await ctx.send(embed=embed)

    @bot.command()
    async def search_giphy(ctx, name):
        giphysearch = giphyobj.search_giphy(name)
        if len(giphysearch) == 0:
            await ctx.send("Nothing was found using the search term {}".format(name))
        else:
            await ctx.send("The following giphys were found with the search term {}\n{}".format(name, giphysearch))

    @bot.command()
    async def list_giphy(ctx):
        giphys = giphyobj.list_giphy()
        await ctx.send("Here is the list of giphys (long lists get concatenated)\n{}".format(giphys))

    bot.run(token)
