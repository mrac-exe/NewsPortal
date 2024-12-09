from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, CategoryList, subscribe
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('news/', cache_page(60*1)(PostList.as_view()), name='post_list'),
    path('news/<int:pk>/', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('news/categories/<int:pk>', CategoryList.as_view(), name='category_list'),
    path('news/categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
