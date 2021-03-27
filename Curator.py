import praw
import os
from dotenv import load_dotenv
load_dotenv()

class Curator:
    def __init__(self,id,secret,name):
        self.reddit = praw.Reddit(
            client_id=id,
            client_secret=secret,
            user_agent="gamer")
        self.curator = self.reddit.redditor(name)
        self.curated = []

    def getPost(self,subreddit):

        for post in self.curator.upvoted(limit = 2):
            if subreddit is not None:
                if post.subreddit == subreddit:
                    if post.id not in self.curated:
                        self.curated.append(post.id)
                        return post



def main():
    curator = Curator(os.getenv("ID"),os.getenv("SECRET"),"Ramenisneat")
    print(curator.getPost("Hentai"))



if __name__ == "__main__":
    main()
