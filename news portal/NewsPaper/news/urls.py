from django.urls import path
from .views import NewsList, NewsDetail, SearchList, NewsCreate, NewsUpdate, NewsDelete


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', SearchList.as_view()),
    path('add/', NewsCreate.as_view(), name='news_create'),
    path('edit/<int:pk>', NewsUpdate.as_view(), name='news_update'),
    path('delete/<int:pk>', NewsDelete.as_view(), name='news_delete'),
]