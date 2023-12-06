from django.urls import path
from .apis import AppApi


urlpatterns = [
    path('apps/', AppApi.as_view(),name="apps"),
]
