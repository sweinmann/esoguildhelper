import discord
import configparser
import http.client


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('bot.conf')
    token = config['DEFAULT']['token']

    client = discord.Client()

    @client.event
    async def on_message(message):
        if message.content.find("!help") != -1:
            await message.channel.send("Help is on the way..")

        if message.content.find("!author") != -1:
            await message.channel.send("Dub created me.")

        if message.content.find("!whydadjoke") != -1:
            await message.channel.send("Annabanana of course.")

        if message.content.find("!dadjoke") != -1:
             conn = http.client.HTTPSConnection("icanhazdadjoke.com")
             headers = {
                 "Accept"      : "text/plain"
             }
             conn.request("GET", "/", headers=headers)
             res = conn.getresponse()
             data = res.read().decode("ascii")

             await message.channel.send(data)

    client.run(token)
