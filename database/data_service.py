from datetime import datetime
from settings import DEV_MODE


class DataSrv:
    """
    Сервис управления данными по подпискам, запросам и результатам
    """

    def subscribe(self, uid: int, name: str, target_id: int):
        pass

    def unsubscribe(self, uid: int, name: str):
        pass

    def is_free_user(self, uid: int):
        return True if not DEV_MODE else False

    def get_targets(self, uid: int) -> list:
        result = []
        return result

    def save_last_tweet_for_user(self, uid: int, target_id: int, tweet_id: int, tweet_timestamp: datetime):
        pass

    def get_last_tweet_for_user(self, uid: int, target_id: int):
        return None
