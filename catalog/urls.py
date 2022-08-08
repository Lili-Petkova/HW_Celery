from django.urls import path

from catalog.views import send_reminder

app_name = "catalog"
urlpatterns = [
    path('reminder/', send_reminder, name='send_reminder'),
]
