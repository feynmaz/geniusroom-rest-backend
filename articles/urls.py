from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'articles'

urlpatterns = [

    path(
        route='',
        view=ArticleListView.as_view(),
        name='list'
    ),
    path(
        route='rubrics/',
        view=RubricView.as_view(),
        name='rubrics',
    ),
    path(
        route='liked/',
        view=ArticlesLiked.as_view(),
        name='liked'
    ),
    path(
        route='<int:pk>/',
        view=ArticleDetailView.as_view(),
        name='detail'
    ),
    path(
        route='<int:pk>/rating/',
        view=RatingView.as_view(),
        name='rating'
    ),
    path(
        route='<int:pk>/rating_by_this_user/',
        view=user_rating,
        name='rating_by_user'
    ),
    path(
        route='<int:pk>/create_comment/',
        view=create_comment,
        name='create_comment'
    ),
    path(
        route='<str:super_rubric_slug>/<str:rubric_slug>/',
        view=ArticleByRubricListView.as_view(),
        name='by_rubric'
    ),

]

urlpatterns = format_suffix_patterns(urlpatterns)