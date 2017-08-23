from django.conf.urls import url
from .views import Bot

urlpatterns = [
    url(r'^f5671e15f50fb97a8a441c8382fa6b9ff9ca5bbd12308d6ccf/?$', Bot.as_view()),
]
