from web_app.views import StateView


routes = [
    ('GET', '/state', StateView, 'get_state'),
]
