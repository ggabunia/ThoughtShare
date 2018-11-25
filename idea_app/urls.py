from django.urls import path
from idea_app import views
from django.conf.urls import include
app_name = 'thought_share'

urlpatterns =[
    path('', views.index, name = 'index'),
    path('ideas/',views.IdeasList.as_view(), name = 'ideas'),
    path('search/',views.SearchIdeas.as_view(), name = 'search'),
    path('register/',views.RegisterForm.as_view(), name = 'register'),
    path('login/',views.LoginForm.as_view(), name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('add-idea/',views.IdeaForm.as_view(), name = 'add_idea'),
    path('my-ideas/',views.my_ideas, name = 'my_ideas'),
]
