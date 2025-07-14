
from django.urls import path
from .import views

urlpatterns = [
    path('',views.chatbox,name='chatbox'),
    path('chat/logout/',views.logout_view,name='logout'),
    path("chat/<str:username>/", views.private_chat, name="private_chat"),
]
