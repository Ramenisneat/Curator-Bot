import praw

class Curator:
    def __init__(self,id,secret,name):
        self.reddit = praw.Reddit(
            client_id=id,
            client_secret=secret,
            user_agent="gamer")
        self.curator = self.reddit.redditor(name)
        self.curated = []

    def getPost(self,subreddit):
        for post in self.curator.upvoted():
            if post.subreddit == subreddit:
                if post.id not in self.curated:
                    self.curated.append(post.id)
                    return post



def main():
    curator = Curator("KqwmYCKEuAJrvA","IwEbSd_jYWZVdlGwo2McncQtr4XKSg","Ramenisneat")



if __name__ == "__main__":
    main()
