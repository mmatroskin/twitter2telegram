from datetime import datetime
from typing import Any

from settings import DEV_MODE


class DataSrv:
    """
    Database service
    """

    def subscribe(self, uid: int, name: str, target_id: int) -> bool:
        return False

    def unsubscribe(self, uid: int, name: str) -> bool:
        return False

    def is_free_user(self, uid: int):
        return True if not DEV_MODE else False

    def get_targets(self, uid: int) -> list:
        result = []
        return result

    def save_last_tweet_for_user(self, uid: int, target_id: int, tweet_id: int, tweet_timestamp: datetime) -> None:
        pass

    def get_last_tweet_for_user(self, uid: int, target_id: int) -> Any:
        return None
