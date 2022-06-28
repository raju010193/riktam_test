from django.urls import path, include
from .views import chat_views, group_views

urlpatterns = [

    path('send-message/', chat_views.ChatAPI.as_view(), name='send_messages'),
    path('users',chat_views.UsersViewsAPI.as_view(),name='users'),
    path('group/', group_views.GroupAPI.as_view(),name='group'),
    path('group/member/', group_views.GroupMembersAPI.as_view(),name='group_member'),
    path('group/chat/', group_views.GroupChatAPI.as_view(),name='group_chat')

]
