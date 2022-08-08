from catalog.views import send_reminder

from django.urls import path

app_name = "catalog"
urlpatterns = [
    path('reminder/', send_reminder, name='send_reminder'),
]
