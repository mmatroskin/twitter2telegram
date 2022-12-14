"""
https://fill.com.ua
"""

from bs4 import BeautifulSoup

from misc.request_srv import get_data


class FillParser:
    _content = None
    url = 'https://fill.com.ua'

    def __init__(self, content):
        try:
            soup = BeautifulSoup(content, 'html.parser')
            self._content = soup.find('video')
        except Exception:
            pass
        if self._content is not None:
            self.success = True
        else:
            self.success = False

    def get_media_data(self):
        video_url = self._content.contents[1].attrs.get('src')
        video_type = self._content.contents[1].attrs.get('type').split('/')[0]
        return f'{self.url}{video_url}', video_type
