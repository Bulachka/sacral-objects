from django.urls import path

from .views import index, by_typ, stone_detail, bibliography, work_detail, author_detail
from .views import StonesCreateView, MentionsCreateView, AuthorsCreateView

urlpatterns = [
    path('add/', StonesCreateView.as_view(), name='add'),
    path('<int:typ_id>/', by_typ, name="by_typ"),
    path('', index, name="index"),
    path('stone_details/<int:pk>/', stone_detail, name='stone_detail'),
    path('mentions/', bibliography, name='bibliography'),
    path('works/<int:pk>/', work_detail, name='work_detail'),
    path('authors/<int:pk>/', author_detail, name='author_detail'),
    path('addPublication/', MentionsCreateView.as_view(), name='addPublication'),
    path('addAuthor/', AuthorsCreateView.as_view(), name='addAuthor'),
]
