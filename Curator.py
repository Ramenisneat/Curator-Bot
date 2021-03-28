import praw
import os
from dotenv import load_dotenv
from prawcore.exceptions import NotFound, Forbidden
from pybooru import Danbooru
load_dotenv()
import requests

class Curator:
    def __init__(self,id,secret,name):
        self.reddit = praw.Reddit(
            client_id=id,
            client_secret=secret,
            user_agent="gamer")
        self.danbooru = Danbooru('danbooru',username = os.getenv("USER"), api_key = os.getenv("API_KEY"))
        self.curator = self.reddit.redditor(name)
        self.curated = []

    def getUpvoted (self,subreddit):
        for post in self.curator.upvoted(limit = 3):
            if subreddit is not None:
                if post.subreddit == subreddit or subreddit == "*":
                    if post.id not in self.curated:
                        self.curated.append(post.id)

                        return post

    def getPost(self,url):
        post = self.reddit.submission(url = url)
        return post

    def getFav(self,id):
        self.danbooru.favorite_add(id)

    def subExists(self,name):
        try:
            sub = self.reddit.subreddits.search_by_name(name)
        except NotFound:
            return False
        else:
            if sub == []:
                return False
            return True

    def userExists(self,name):
        try:
            temp = self.reddit.redditor(name).id
            print(temp)
            temp.upvoted()
        except NotFound or Forbidden:
            return False
        else:
            if temp == []:
                return False
            return True


def main():
    curator = Curator(os.getenv("ID"),os.getenv("SECRET"),"Ramenisneat")
    post = curator.getUpvoted("*")
    # curator.getFav(443643)
    print(curator.danbooru.favorite_list(802693))


if __name__ == "__main__":
    main()
