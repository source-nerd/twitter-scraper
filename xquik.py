import datetime
import json
import os
import urllib.error
import urllib.parse
import urllib.request
import uuid

from tweets import Tweet


XQUIK_BASE_URL = "https://xquik.com"
XQUIK_SEARCH_PATH = "/api/v1/x/tweets/search"
_ALLOWED_HOSTS = {"xquik.com"}
_QUERY_TYPES = {"Latest", "Top"}


def _int_or_zero(value):
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return 0
    return 0


def _parse_date(value):
    if not isinstance(value, str) or value == "":
        return datetime.datetime.utcfromtimestamp(0)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.datetime.fromisoformat(normalized)
    except ValueError:
        return datetime.datetime.utcfromtimestamp(0)
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return parsed


def _tweet_from_xquik(raw):
    author = raw.get("author") if isinstance(raw.get("author"), dict) else {}
    return Tweet(
        str(uuid.uuid4()),
        str(author.get("name", "")),
        str(author.get("username", "")),
        str(raw.get("id", "")),
        str(raw.get("text", "")),
        _parse_date(raw.get("createdAt")),
        _int_or_zero(raw.get("retweetCount")),
        _int_or_zero(raw.get("likeCount")),
        str(raw.get("url", "")),
    )


class XquikClient:
    def __init__(self, api_key=None, base_url=XQUIK_BASE_URL, timeout=15):
        key = api_key or os.environ.get("XQUIK_API_KEY")
        if not key:
            raise ValueError("Xquik API key required. Pass api_key or set XQUIK_API_KEY.")

        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS:
            raise ValueError("Xquik base URL must use https://xquik.com.")

        self.api_key = key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search(self, search_query, max_results=20, query_type="Latest"):
        if query_type not in _QUERY_TYPES:
            raise ValueError("query_type must be Latest or Top.")
        if max_results < 1:
            raise ValueError("max_results must be at least 1.")

        params = urllib.parse.urlencode(
            {
                "q": search_query,
                "queryType": query_type,
                "limit": min(max_results, 200),
            }
        )
        request = urllib.request.Request(
            self.base_url + XQUIK_SEARCH_PATH + "?" + params,
            headers={
                "Accept": "application/json",
                "User-Agent": "source-nerd-twitter-scraper Xquik helper",
                "x-api-key": self.api_key,
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            raise RuntimeError("Xquik search failed with HTTP {}.".format(error.code))

        tweets = payload.get("tweets") if isinstance(payload, dict) else None
        if not isinstance(tweets, list):
            raise RuntimeError("Xquik search returned an invalid response.")

        return [_tweet_from_xquik(tweet) for tweet in tweets if isinstance(tweet, dict)]


def search_tweets(search_query, api_key=None, max_results=20, query_type="Latest"):
    return XquikClient(api_key=api_key).search(
        search_query,
        max_results=max_results,
        query_type=query_type,
    )
