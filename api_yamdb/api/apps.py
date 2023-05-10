from django.apps import AppConfig
from django.dispatch import Signal

from api.utilites import send_confirm_code, update_title_rating


class ApiV1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


def update_title_rating_dispatcher(sender, **kwargs):
    title_id = kwargs.get('title_id', None)
    if title_id is None:
        return
    update_title_rating(title_id)


def user_registered_dispatcher(sender, **kwargs):
    send_confirm_code(kwargs['instance'])


signal_need_update_rating = Signal()
signal_need_update_rating.connect(update_title_rating_dispatcher)

signal_user_registered = Signal()
signal_user_registered.connect(user_registered_dispatcher)
