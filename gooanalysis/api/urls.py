from django.urls import path, include

urlpatterns = [
    path('analysis/', include(('gooanalysis.applists.urls', 'applists')))
]
