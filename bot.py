import discord
import configparser

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

    client.run(token)
