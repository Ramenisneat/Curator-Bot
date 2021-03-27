import discord
from dotenv import load_dotenv

load_dotenv()
import os
import Curator
from asyncio import sleep

Subreddit = None
Redditor = None
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
                post = curator.getPost(Subreddit)
                if post is not None:
                    e = discord.Embed(title=post.title, description="https://www.reddit.com/" + post.permalink,
                                      color=0xFF5700)
                    e.set_image(url=post.url)
                    channel = client.get_channel(Channel)
                    await channel.send(embed=e)

            await sleep(10)

    @client.event
    async def on_ready():
        print("ready")
        # Creates custome coroutine
        client.loop.create_task(upvoteStream())

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
                Redditor = message.content[9:]
                curator = Curator.Curator(os.getenv("ID"), os.getenv("SECRET"), Redditor)
                await message.channel.send(f"Curator set to {Redditor}")

            if message.content[5:8] == "sub":
                Subreddit = message.content[9:]
                await message.channel.send(f"Subreddit set to {Subreddit}")
            if message.content[5:8] == "cha":
                Channel = int(message.content[9:])
                await (client.get_channel(Channel)).send("Channel set to here")


    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
