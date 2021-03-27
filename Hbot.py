import discord
from dotenv import load_dotenv
import os
import Curator
from asyncio import sleep
import re

load_dotenv()

Subreddit = "Hentai"
Redditor = "Ramenisneat"
Channel = None
curator = None


def main():
    # curator = Curator.Curator(os.getenv("ID"), os.getenv("SECRET"), os.getenv("REDDITOR"))
    client = discord.Client()

    async def upvoteStream():
        global curator
        global Channel
        global Subreddit
        while True:
            if curator is not None and Subreddit is not None and Channel is not None:
                post = curator.getUpvoted(Subreddit)
                if post is not None:
                    # print(post.url)
                    if "v." in post.url:
                        # print(post.url)
                        e = discord.Embed(title=post.title, description="https://www.reddit.com/" + post.permalink,
                                          color=0xFF5700)
                    else:
                        e = discord.Embed(title=post.title, description="https://www.reddit.com/" + post.permalink,
                                      color=0xFF5700)

                        e.set_image(url=post.url)

                    channel = client.get_channel(Channel)
                    await channel.send(embed=e)

            await sleep(10)

    async def getSauce(post):
        global Channel
        sauce = post.comments[0]
        if sauce.author != "HentaiSauce_Bot":
            await client.get_channel(Channel).send(
                "HentaiSauce_Bot was not able to find the sauce. I recommend using Saucenao, IQDB and/or Tineye yourself.")
        else:
            links = re.search("Image links.*\n", post.comments[0].body)
            links = links.group(0)[15:-3]
            links = links.split(" | ")
            e = discord.Embed(title="Sauce from HentaiSauce_Bot", description="\n".join(
                links) + "Please be aware the Hentaisauce_bot is not 100% accurate and doesn't account for post deletions.",
                              color=0x800080, image="https://www.userlogos.org/files/logos/zoinzberg/SauceNAO.png")
            await client.get_channel(Channel).send(embed=e)

    @client.event
    async def on_ready():
        global curator
        global Redditor
        print("ready")
        # Creates custome coroutine
        client.loop.create_task(upvoteStream())
        if Redditor is not None:
            curator = Curator.Curator(os.getenv("ID"), os.getenv("SECRET"), Redditor)

    @client.event
    async def on_message(message):
        global curator
        global Subreddit
        global Redditor
        global Channel
        if message.author == client.user:
            return
        if message.content.startswith("~get"):
            if curator is not None and Subreddit is not None:
                post = curator.getPost(Subreddit)
                e = discord.Embed(title=post.title, description=post.permalink, color=0xFF5700, image=post.url)
                e.set_image(url=post.url)
                print(post.url)
                await message.channel.send(embed=e)
            else:
                await message.channel.send(
                    "Please set the Subreddit and/or the Redditor. You may also have to set the Channel")

        elif message.content.startswith("~set"):
            if message.content[5:8] == "red":
                check = curator.userExists(message.content[9:])
                if check:
                    Redditor = message.content[9:]
                    curator = Curator.Curator(os.getenv("ID"), os.getenv("SECRET"), Redditor)
                    await message.channel.send(f"Curator set to {Redditor}")
                else:
                    await message.channel.send(
                        f"{message.content[9:]} not found/cannot be accessed, please check for typos")

            elif message.content[5:8] == "sub":
                check = curator.subExists(message.content[9:])
                if check:
                    Subreddit = message.content[9:]
                    await message.channel.send(f"Subreddit set to {Subreddit}")

                else:
                    await message.channel.send(
                        f"{message.content[9:]} not found/cannot be accessed, please check for typos. (The redditor must make their upvotes public)")

            elif message.content[5:8] == "cha":
                Channel = int(message.content[9:])
                if client.get_channel(Channel) is None:
                    await message.channel.send(
                        "Channel not found. Channel's must be set using their correponding id's.")
                    Channel = None
                elif type(client.get_channel(Channel)) is not discord.channel.TextChannel:
                    await message.channel.send("Channels can only be set to text channels.")
                    Channel = None
                else:
                    await (client.get_channel(Channel)).send("Channel set to here")

            else:
                message.channel.send("Command not found")


        elif message.content.startswith("~current"):
            e = discord.Embed(title="Current config", color=0xC0C0C0)
            e.add_field(name="Redditor", value=Redditor)
            e.add_field(name="Subreddit", value=Subreddit)
            e.add_field(name="Channel", value=client.get_channel(Channel))
            e.add_field(name="Channel ID", value=Channel)
            await message.channel.send(embed=e)

        elif message.content.startswith("~help"):
            e = discord.Embed(title="help", color=0xC0C0C0)
            e.add_field(name="~set sub <subreddit>",
                        value="Sets the bot's target subreddit. You can set the subreddit to '*' to get all of their upvoted post")
            e.add_field(name="~set red <redditor>", value="Sets the bot's target redditor.")
            e.add_field(name="~set cha <channelID>",
                        value="Sets the bot's target text channel. You can get the ID of a text channel by right clicking it and selecting 'Copy ID'.")
            e.add_field(name="~curent", value="Displays current settings.")
            e.add_field(name="Get Sauce", value="Displays current settings.")

            await message.channel.send(embed=e)

    @client.event
    async def on_reaction_add(reaction, user):
        global curator
        if reaction.emoji == "😏":
            if reaction.message.author is client:
                return
            else:
                e = reaction.message.embeds
                url = e[0].description
                post = curator.getPost(url)
                if post.subreddit == "hentai":
                    await getSauce(post)
                else:
                    await reaction.message.channel.send("Sauce can only be found with posts from r/Hentai")

    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
