from django.urls import path
from .views import MessageListCreateView

urlpatterns = [
    path('match/<int:match_id>/messages/', MessageListCreateView.as_view(), name='messages'),
]
