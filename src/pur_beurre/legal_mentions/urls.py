from django.urls import path
from .views import LegalMentionsView

app_name = 'legal_mentions'

urlpatterns = [
    path('', LegalMentionsView.as_view(), name='legal_mentions'),
]
