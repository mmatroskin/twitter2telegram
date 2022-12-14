from aiogram.dispatcher.filters.state import State, StatesGroup


class SubscribeForm(StatesGroup):
    """

    """
    username = State()


class UserTweetsWithoutSubscribeForm(StatesGroup):
    """

    """
    username = State()
