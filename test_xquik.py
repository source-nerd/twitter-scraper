import json
import unittest
from urllib.error import HTTPError
from unittest import mock

from xquik import XquikClient, search_tweets


class Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class XquikClientTest(unittest.TestCase):
    def test_search_maps_tweets(self):
        seen = {}

        def fake_urlopen(request, timeout):
            seen["url"] = request.full_url
            seen["key"] = request.headers["X-api-key"]
            seen["timeout"] = timeout
            return Response(
                {
                    "tweets": [
                        {
                            "id": "123",
                            "text": "hello",
                            "createdAt": "2026-01-02T03:04:05Z",
                            "likeCount": 7,
                            "retweetCount": 2,
                            "url": "https://x.com/alice/status/123",
                            "author": {
                                "username": "alice",
                                "name": "Alice",
                            },
                        }
                    ]
                }
            )

        with mock.patch("xquik.urllib.request.urlopen", fake_urlopen):
            tweets = XquikClient("test-key", timeout=4).search(
                "launch",
                max_results=5,
                query_type="Top",
            )

        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0].tweet_id, "123")
        self.assertEqual(tweets[0].tweet, "hello")
        self.assertEqual(tweets[0].name, "Alice")
        self.assertEqual(tweets[0].screen_name, "alice")
        self.assertEqual(tweets[0].retweet_count, 2)
        self.assertEqual(tweets[0].favourites_count, 7)
        self.assertIn("q=launch", seen["url"])
        self.assertIn("queryType=Top", seen["url"])
        self.assertEqual(seen["key"], "test-key")
        self.assertEqual(seen["timeout"], 4)

    def test_requires_api_key(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "API key required"):
                XquikClient()

    def test_search_tweets_uses_client(self):
        with mock.patch.object(XquikClient, "search", return_value=["tweet"]) as search:
            result = search_tweets("launch", api_key="test-key", max_results=3)

        self.assertEqual(result, ["tweet"])
        search.assert_called_once_with("launch", max_results=3, query_type="Latest")

    def test_http_error_omits_api_key(self):
        def fake_urlopen(request, timeout):
            raise HTTPError(request.full_url, 401, "Unauthorized", hdrs=None, fp=None)

        with mock.patch("xquik.urllib.request.urlopen", fake_urlopen):
            with self.assertRaisesRegex(RuntimeError, "HTTP 401") as ctx:
                XquikClient("test-key").search("launch")

        self.assertNotIn("test-key", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
