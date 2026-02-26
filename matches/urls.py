from django.urls import path
from .views import (
    SuggestionView,
    SwipeView,
    MatchListView,
    SendMessageView,
    MessageListView
)

urlpatterns = [
    path("suggestions/", SuggestionView.as_view()),
    path("swipe/", SwipeView.as_view()),
    path("matches/", MatchListView.as_view()),
    path("chat/<int:match_id>/send/", SendMessageView.as_view()),
    path("chat/<int:match_id>/", MessageListView.as_view()),
]