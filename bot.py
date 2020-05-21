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
        if messgae.content.find("!whydadjoke") != -1:
            await message.channel.send("Annabanana of course.")
        if messsage.content.find("!dadjoke") != -1:
            conn = http.client.HTTPSConnection("dad-jokes.p.rapidapi.com")
            headers = {
                'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
                'x-rapidapi-key' : "0ad692458cmsh7fec2bdb1575ca3p19c718jsne9f90cc31d76"
            }
            conn.request("GET", "random/jokes", headers=headers)

            res=conn.getresponse()
            joke=res.read()
            await message.channel.send(joke.decode("utf-8"))

    client.run(token)
