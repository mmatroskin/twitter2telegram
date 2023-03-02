from __future__ import annotations

import re
from os.path import join
from time import sleep
from typing import List, Dict

from requests import Request, sessions, exceptions

from helpers import dict_to_url
from logger import get_logger
from parsers.exceptions import RefreshTokenException
from parsers.tweet import Tweet, MediaType
from settings import ROOT_DIR, LOG_FILE, DATA_DIR, TWITTER_TOKEN, MAIN_JS_URL, DEMO_COUNT, DEV_MODE


class Parser:
    _base_url: str = 'https://twitter.com'
    _api_url = 'https://api.twitter.com'
    _method: str = 'GET'
    _retries: int = 5
    _timeout: int = 10
    _main_js_url = MAIN_JS_URL
    _bearer = TWITTER_TOKEN
    _token: str | None = None
    demo_count = DEMO_COUNT
    count = 30
    logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)

    def __init__(self, getting_token_with_web=True):
        self.getting_token_with_web = getting_token_with_web
        self._session = sessions.Session()
        self._session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'})
        self._set_token()
        self._session.headers.update({"x-guest-token": self._token})
        self.logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)

    def close_session(self):
        self._session.close()

    def get_tweets(self, rest_id: str = None, username: str = None, exclude_replies: bool = False,
                   start_time: str = None, count: int = None, since_id: int = None, demo: bool = True) -> List[Tweet]:

        def tweets_sort(item):
            return item.id

        query_base = f'from:{username} ' if username else ''
        # query_base = f'{query_base} since: {start_time} ' if start_time else query_base
        rep = 'filter' if exclude_replies else 'exclude'
        query = f'{query_base}{rep}:replies exclude:nativeretweets exclude:retweets'

        params = {
            "include_profile_interstitial_type": "1",
            "include_blocking": "1",
            "include_blocked_by": "1",
            "include_followed_by": "1",
            "include_want_retweets": "1",
            "include_mute_edge": "1",
            "include_can_dm": "1",
            "include_can_media_tag": "1",
            "skip_status": "1",
            "cards_platform": "Web-12",
            "include_cards": "1",
            "include_ext_alt_text": "true",
            "include_quote_count": "true",
            "include_reply_count": "1",
            "tweet_mode": "extended",
            "include_entities": "true",
            "include_user_entities": "true",
            "include_ext_media_color": "true",
            "include_ext_media_availability": "true",
            "result_type": "recent",
            "send_error_codes": "true",
            "simple_quoted_tweet": "true",
            "q": query,
            "tweet_search_mode": "live",
            "query_source": "typed_query",
            "pc": "1",
            "spelling_corrections": "1",
            "ext": "mediaStats,highlightedLabel",
        }
        if not username and rest_id:
            params["user_id"] = rest_id

        if not count:
            count = self.count
        if demo:
            count = self.demo_count
        params["count"] = count

        # not work
        # if since_id:
        #     params["since_id"] = str(since_id)

        result = []
        tweets = self._get_tweets(**params)
        if tweets is None:
            return result
        for uid, item in tweets.items():
            if not since_id or uid > since_id:
                item['user_name'] = username
                tweet = Tweet(**item)
                if tweet.is_root:
                    result.append(tweet)
        if result:
            result.sort(key=tweets_sort)
            result = self._set_media_blobs(result)
        if DEV_MODE and since_id:
            print('Check ids: ')
            for c, i in enumerate(result):
                if i.id <= since_id:
                    print(c, i.id, i.url)
        return result

    def get_user_id(self, username: str) -> int | None:
        dct = {'screen_name': username, 'withHighlightedLabel': False}
        route = 'graphql/jMaTS-_Ea8vh9rpKggJbCQ/UserByScreenName?variables=%s' % dict_to_url(dct)
        req = self._session.prepare_request(Request(self._method, f'{self._api_url}/{route}'))
        response = self._session.send(req, allow_redirects=True, timeout=self._timeout)
        if response.status_code != 200:
            self.logger.error(response.text)
            return None
        if response.json().get('errors'):
            return None
        return int(response.json()['data']['user']['rest_id'])

    def _get_tweets(self, **kwargs) -> Dict | None:
        # route = f'2/timeline/{rest_id}/tweets'
        # route = f'2/timeline/profile/{rest_id}.json?userId={rest_id}&count={self.count}'
        route = f'2/search/adaptive.json'
        # route = f'2/tweets/search/recent'

        req = self._session.prepare_request(Request(self._method, f'{self._api_url}/{route}', params=kwargs))
        response = self._session.send(req, timeout=self._timeout)
        if response.status_code != 200:
            self.logger.error(response.reason)
            return None
        objects = response.json().get('globalObjects')
        return objects.get('tweets') if objects else {}

    def _set_media_blobs(self, tweets: List[Tweet]):
        for i in tweets:
            for j in i.media:
                if j.type != MediaType.photo.value:
                    req = self._session.prepare_request(Request(self._method, j.media_url))
                    response = self._session.send(req, timeout=self._timeout)
                    if response.status_code == 200:
                        j.blob = response.content
                    else:
                        self.logger.error(response.reason)
        return tweets

    def _set_token_base(self):
        main_js_res = None
        try:
            main_js_res = self._session.get(self._main_js_url, timeout=self._timeout)
        except Exception as exc:
            self.logger.error(str(exc))
        if main_js_res and main_js_res.status_code == 200:
            match = re.search(r"s=\"([\w\%]{104})\"", main_js_res.text)
            self._bearer = f'Bearer {match[1]}'
        self._session.headers.update({"authorization": self._bearer})
        route = "1.1/guest/activate.json"
        try:
            res = self._session.post(f'{self._api_url}/{route}')
            if res.status_code == 200:
                guest_token = res.json()
                self._token = guest_token.get('guest_token')
        except Exception as exc:
            self.logger.error(str(exc))

    def _set_token(self):
        self._set_token_base()
        if not self._token:
            msg = 'Could not get the Guest token from API 1.1'
            if self.getting_token_with_web:
                self.logger.error(f'{msg}, try with web page')
                self.logger.error(msg)
                self._set_token_with_web_page()
            else:
                raise RefreshTokenException(msg)

    def _set_token_with_web_page(self):
        for attempt in range(self._retries + 1):
            req = self._session.prepare_request(Request(self._method, self._base_url))
            try:
                res = self._session.send(req, allow_redirects=True, timeout=self._timeout)
            except exceptions.RequestException as exc:
                if attempt < self._retries:
                    retrying = ', retrying'
                else:
                    retrying = ''
                self.logger.info(f'Error retrieving {req.url}: {exc!r}{retrying}')
            else:
                match = re.search(r'\("gt=(\d+);', res.text)
                if match:
                    self._token = str(match.group(1))
                    break
                else:
                    self._token = None
                    raise RefreshTokenException('Could not find the Guest token in HTML')

            if attempt < self._retries:
                sleep_time = 2.0 * 2 ** attempt
                self.logger.info(f'Waiting {sleep_time:.0f} seconds...')
                sleep(sleep_time)

        else:
            msg = f'{self._retries + 1} requests to {self._base_url} failed, giving up.'
            self.logger.error(msg)
            self._token = None
            raise RefreshTokenException(msg)
