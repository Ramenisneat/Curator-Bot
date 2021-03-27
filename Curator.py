import praw
import os
from dotenv import load_dotenv
from prawcore.exceptions import NotFound, Forbidden
load_dotenv()

class Curator:
    def __init__(self,id,secret,name):
        self.reddit = praw.Reddit(
            client_id=id,
            client_secret=secret,
            user_agent="gamer")
        self.curator = self.reddit.redditor(name)
        self.curated = []

    def getUpvoted (self,subreddit):
        for post in self.curator.upvoted(limit = 2):
            if subreddit is not None:
                if post.subreddit == subreddit or subreddit == "*":
                    if post.id not in self.curated:
                        self.curated.append(post.id)
                        return post

    def getPost(self,url):
        post = self.reddit.submission(url = url)
        return post

    def subExists(self,name):
        try:
            self.reddit.subreddits.search_by_name(name)
        except NotFound:
            return False
        return True

    def userExists(self,name):
        try:
            temp = self.reddit.redditor(name)
            temp.upvoted()
        except NotFound or Forbidden:
            return False
        return True









def main():
    curator = Curator(os.getenv("ID"),os.getenv("SECRET"),"Ramenisneat")
    post = curator.getUpvoted("*")





if __name__ == "__main__":
    main()
