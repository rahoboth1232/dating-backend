from django.urls import path
from .views import SwipeView, MatchListView

urlpatterns = [
    path('swipe/', SwipeView.as_view(), name='swipe'),
    path('matches/', MatchListView.as_view(), name='matches'),
]
