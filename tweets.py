class Tweet:
    def __init__(self, uuid, name, screen_name, tweet_id, tweet, date_time, retweet_count, favourites_count, link):
        self.uuid = uuid
        self.name = name
        self.screen_name = screen_name
        self.tweet_id = tweet_id
        self.tweet = tweet
        self.date_time = date_time
        self.retweet_count = retweet_count
        self.favourites_count = favourites_count
        self.link = link
