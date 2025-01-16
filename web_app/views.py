from os.path import join
from aiohttp import web
from logger import get_logger
from settings import ROOT_DIR, LOG_FILE, MESSAGE_SUCCESS, MESSAGE_ERROR, MESSAGE_404, MESSAGE_BAD_QUERY


logger = get_logger(join(ROOT_DIR, LOG_FILE), 'web_app')


class BaseView(web.View):

    def __init__(self, *args, **kwargs):
        super(web.View, self).__init__(*args, **kwargs)
        self.result = {
            'success': False,
            'message': MESSAGE_BAD_QUERY,
            'data': None
        }


class StateView(BaseView):

    async def get(self):
        result = self.result.copy()
        result['success'] = True
        result['message'] = MESSAGE_SUCCESS
        result['data'] = {'bot': None, 'worker':  None}
        response = web.json_response(result)
        return response
