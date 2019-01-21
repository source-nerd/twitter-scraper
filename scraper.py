import datetime
import http.cookiejar
import json
import re
import uuid
import urllib.parse, urllib.request, urllib.error
from pyquery import PyQuery
from tweets import Tweet


def get_tweets(search_params, current_position):
    """
    Build search Query and get the tweets
    :param search_params: SearchParams object
    :param current_position: Min position where you want to retrieve the tweets from
    :return: twitter json_data
    """
    base_url = "https://twitter.com/i/search/timeline?f=tweets&q={}&src=typd&{}max_position={}"
    query = ''
    query = query + (' ' + search_params.search_query) if search_params.search_query else query
    query = query + (' from:' + search_params.account_name) if search_params.account_name else query
    query = query + (' since:' + search_params.since_date) if search_params.since_date else query
    query = query + (' until:' + search_params.until_date) if search_params.until_date else query
    lang = ('lang=' + search_params.language + '&') if search_params.language else ''

    query = urllib.parse.quote(query)
    base_url = base_url.format(query, lang, current_position)
    print(base_url)

    cookie_jar = http.cookiejar.CookieJar()
    headers = [
        ('Host', "twitter.com"),
        ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
        ('Accept', "application/json, text/javascript, */*; q=0.01"),
        ('Accept-Language', "en-US;q=0.7,en;q=0.3"),
        ('X-Requested-With', "XMLHttpRequest"),
        ('Referer', base_url),
        ('Connection', "keep-alive")
    ]

    attempts = 0
    response = ''
    while attempts < 10:
        try:
            if search_params.proxy:
                print('Using IP {}'.format(search_params.proxy))
                proxy = urllib.request.ProxyHandler({'http': search_params.proxy, 'https': search_params.proxy})
                opener = urllib.request.build_opener(proxy, urllib.request.HTTPCookieProcessor(cookie_jar))
            else:
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
            opener.addheaders = headers
            response = opener.open(base_url)
            break
        except Exception:
            attempts += 1
            print('Retrying with different IP !!')

    json_res = response.read()
    json_data = json.loads(json_res.decode())
    return json_data


def parse_json(search_params):
    """
    Parse the json tweet
    :param search_params: SearchParams object
    :return: void
    """
    min_position = get_last_search_position(search_params.log_file_name)
    count = 0
    while True:
        json_res = get_tweets(search_params, min_position)
        if len(json_res['items_html'].strip()) == 0:
            break

        min_position = json_res['min_position']
        search_params.logging.info('min_pos - {}'.format(min_position))
        item = json_res['items_html']
        scraped_tweets = PyQuery(item)
        scraped_tweets.remove('div.withheld-tweet')
        tweets = scraped_tweets('div.js-stream-tweet')

        for tweet_html in tweets:
            print(count)
            tweet_py_query = PyQuery(tweet_html)
            name = tweet_py_query.attr("data-name")
            screen_name = tweet_py_query.attr("data-screen-name")
            tweet_id = tweet_py_query.attr("data-tweet-id")
            tweet_text = re.sub(r"\s+", " ",
                                tweet_py_query("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
            tweet_date_time = int(tweet_py_query("small.time span.js-short-timestamp").attr("data-time"))
            tweet_date_time = datetime.datetime.fromtimestamp(tweet_date_time)
            retweet_count = int(tweet_py_query("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr(
                "data-tweet-stat-count").replace(",", ""))
            favorites_count = int(
                tweet_py_query("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr(
                    "data-tweet-stat-count").replace(",", ""))
            permalink = 'https://twitter.com' + tweet_py_query.attr("data-permalink-path")

            tweet = Tweet(str(uuid.uuid4()), name, screen_name, tweet_id, tweet_text, tweet_date_time, retweet_count,
                          favorites_count, permalink)
            # Now Write to OP or save to DB
            write_op(search_params.op, tweet)
            count += 1
        # sleep(5)
        if 0 < search_params.max_retrieval_count <= count:
            break


def write_op(op_file, tweet):
    """
    Writing tweets to some output file
    :param op_file: op_file name
    :param tweet: Tweet object
    :return: void
    """
    with open(op_file, 'a+', encoding='utf-8') as f:
        # UUID, tweet_id, user_name, screen_name, tweet, date_time, retweet_count, fav_count, link
        f.write(
            ('%s;%s;%s;%s;%s;%s;%d;%d;%s\n' % (tweet.uuid, tweet.tweet_id, tweet.name, tweet.screen_name, tweet.tweet,
                                               tweet.date_time.strftime("%Y-%m-%d %H:%M"), tweet.retweet_count,
                                               tweet.favourites_count, tweet.link)))


def get_last_search_position(logger_file):
    """
    Required for resuming the previous search operation
    :param logger_file: Logger file name
    :return: Last position id
    """
    with open(logger_file, 'r+') as f:
        lines = f.read().splitlines()
        try:
            last_pos = lines[-1].split(' - ')[1]
        except IndexError:
            last_pos = ''
        return last_pos
