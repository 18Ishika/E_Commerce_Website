from django.urls import path
from .views import chatbot_api,chatbot_test_page

urlpatterns = [
    path("chatbot/", chatbot_api, name="chatbot_api"),
    path("test/", chatbot_test_page, name="chatbot_test"),
]
