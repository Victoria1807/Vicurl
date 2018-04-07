from django.conf.urls import url
from .views import wildcart_redirect

urlpatterns = [
    url(r'^(?P<path>.*)', wildcart_redirect),
]
