"""

"""
import datetime
from enum import Enum
from typing import List, Any, Optional


class MediaType(Enum):
    photo = 1
    video = 2
    animated_gif = 3
    audio = 4


class Media:
    id: int
    name: str = None
    media_url: str
    url: str
    display_url: str
    expanded_url: str
    type: int
    blob: bytes = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        self.name = self.media_url.split('/')[-1] if self.media_url else 'Unknown media'


class Tweet:
    id: int
    created_at: datetime.datetime
    user_id: int
    user_name: str
    conversation_id: int
    url: str
    full_text: str
    in_reply_to_status_id: int
    in_reply_to_user_id: int
    in_reply_to_screen_name: str
    entity_urls: List[str]
    entity_hashtags: List[str]
    entity_symbols: List[Any]
    media: List[Media]
    is_root: bool
    _url_template: str = 'https://twitter.com/%s/status/%d'

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.created_at = datetime.datetime.strptime(kwargs['created_at'], '%a %b %d %H:%M:%S %z %Y')
        self.user_id = kwargs['user_id']
        self.user_name = kwargs['user_name']
        self.conversation_id = kwargs.get('conversation_id')
        self.full_text = kwargs['full_text']
        self.in_reply_to_status_id = kwargs.get('in_reply_to_status_id')
        self.in_reply_to_user_id = kwargs.get('in_reply_to_user_id')
        self.in_reply_to_screen_name = kwargs.get('in_reply_to_screen_name')
        self.entity_hashtags = kwargs['entities'].get('hashtags') if kwargs.get('entities') else []
        self. entity_symbols = kwargs['entities'].get('symbols') if kwargs.get('entities') else []
        self.is_root = self.id == self.conversation_id

        self.url = self._url_template % (kwargs['user_name'], kwargs['id']) if self.is_root else ''

        urls = kwargs['entities'].get('urls', []) if kwargs.get('entities') else []
        self.entity_urls = self._get_entity_urls(urls)

        # media = kwargs['entities'].get('media', []) if kwargs.get('entities') else []
        media = kwargs['extended_entities'].get('media', []) if kwargs.get('extended_entities') else []
        self.media = self._get_entity_media(media)

        ents = urls + media
        self._clean_full_text(ents)

    def _clean_full_text(self, urls: List[dict]):
        for item in urls:
            self.full_text = self.full_text.replace(item['url'], '')
        self.full_text = self.full_text.strip()

    def _get_entity_urls(self, urls: Optional[List[dict]]):
        result = []
        for item in urls:
            if item.get('expanded_url'):
                result.append(item['expanded_url'])
        return result

    def _get_entity_media(self, media: Optional[List[dict]]):
        result = []
        for item in media:
            media_type = MediaType[item['type']]
            url = item['media_url_https']
            if media_type == MediaType.video or media_type == MediaType.animated_gif:
                video_info = item.get('video_info')
                if video_info:
                    variants = video_info.get('variants')
                    variants.sort(key=lambda x: x.get('bitrate', 0))
                    url = variants[-1]['url'].rsplit('?tag')[0]
                else:
                    media_type = MediaType.photo
            result.append(Media(id=item['id'],
                                media_url=url,
                                url=item['url'],
                                display_url=item['display_url'],
                                expanded_url=item['expanded_url'],
                                type=media_type.value))
        return result
