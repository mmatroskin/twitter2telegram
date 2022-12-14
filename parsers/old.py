import re
from os.path import join
from time import sleep
from typing import Union, Any, List, Dict

import twint
import tweepy
from requests import Request, sessions, exceptions

from helpers import get_start_time, get_end_time, dict_to_url
from logger import get_logger
from parsers.exceptions import RefreshTokenException
from settings import ROOT_DIR, LOG_FILE, DATA_DIR, TWITTER_TOKEN, MAIN_JS_URL, DEMO_COUNT, DEV_MODE


class TwintParser:
    _username = None
    _user = None
    logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)

    def __init__(self, username):
        self._username = username

    def get_config(self):
        config = twint.Config()
        config.Username = self._username
        config.Store_object = True
        config.User_full = True
        config.Filter_retweets = True
        config.Images = True
        config.Videos = True
        # config.Debug = True
        return config

    def get_tweets(self) -> list:
        config = self.get_config()
        config.Since = get_start_time()
        config.Until = get_end_time()
        # config.Limit = 2
        # config.Search = 'to help mend the fault in our stars'

        twint.run.Search(config)
        tweets = twint.output.tweets_list
        return tweets

    def get_user_id(self) -> Union[str, None]:
        config = self.get_config()
        try:
            twint.run.Lookup(config)
        except Exception as exc:
            self.logger.error(str(exc))
        else:
            self._user = twint.output.users_list[0]
        return self._user.id if self._user else None

    def _user_object_serialiser(self, user: object):
        result = {}
        for k, v in user.__dict__.items():
            result[k] = v
        return result


class TweepyParser:
    _client: tweepy.Client = None
    _base_url: str = 'https://twitter.com'
    _method: str = 'GET'
    _retries: int = 5
    _timeout: int = 15
    _token: str = None
    logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)

    def __init__(self):
        self._set_token()
        _headers = [("authorization", TWITTER_TOKEN), ("x-guest-token", self._token)]
        self._client = tweepy.Client(TWITTER_TOKEN)
        self.logger = get_logger(join(ROOT_DIR, LOG_FILE), __name__)

    def get_tweets(self, user_id: str) -> List[Any] | None:
        response = self._client.get_users_tweets(user_id)
        if response.errors:
            self.logger.error(response.errors)
            return None
        return response.data

    def get_user_id(self, username: str) -> str | None:
        user = self.get_user_info(username)
        return user.id if user else None

    def get_user_info(self, username: str) -> Any | None:
        response = self._client.get_users(usernames=[username])
        if response.errors:
            self.logger.error(response.errors)
            return None
        return response.data

    def _set_token(self):
        session = sessions.Session()
        session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'})

        for attempt in range(self._retries + 1):
            req = session.prepare_request(Request(self._method, self._base_url))
            try:
                res = session.send(req, allow_redirects=True, timeout=self._timeout)
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
