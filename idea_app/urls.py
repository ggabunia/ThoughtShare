from django.urls import path
from idea_app import views
from django.conf.urls import include
app_name = 'thought_share'

urlpatterns =[
    path('', views.index, name = 'index'),
    path('ideas',views.IdeasList.as_view(), name = 'ideas'),
    path('search',views.SearchIdeas.as_view(), name = 'search')
]
