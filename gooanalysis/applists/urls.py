from django.urls import path
from .apis import AppApi,AppDetailApi


urlpatterns = [
    path('apps/', AppApi.as_view(),name="apps"),
    path('apps/<str:app_id>', AppDetailApi.as_view(),name="appdetail"),

]
