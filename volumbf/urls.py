from django.urls import path

from .views import index, by_typ, bibliography, work_detail, AuthorDetail, add_comment_to_stone, post_share
#author_detail, stone_detail,
from .views import StonesCreateView, MentionsCreateView, AuthorsCreateView, StonesDetail, StonesImageUpload

urlpatterns = [
    path('add/', StonesCreateView.as_view(), name='add'),
    path('<int:typ_id>/', by_typ, name="by_typ"),
    path('', index, name="index"),
    #path('stone_details/<int:pk>/', stone_detail, name='stone_detail'),
    path('stone_details/<int:pk>/', StonesDetail.as_view(), name='stone_detail'),
    path('stone/<int:stones_id>/image/upload', StonesImageUpload.as_view(), name='StonesImageUpload'),
    path('mentions/', bibliography, name='bibliography'),
    path('works/<int:pk>/', work_detail, name='work_detail'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='authors_detail'),
    #path('authors/<int:pk>/', author_detail, name='authors_detail'),
    path('addPublication/', MentionsCreateView.as_view(), name='addPublication'),
    path('addAuthor/', AuthorsCreateView.as_view(), name='addAuthor'),
    path('stone/<int:pk>/comment/', add_comment_to_stone, name='add_comment_to_stone'),
    path('stone/<int:pk>/share/', post_share, name='post_share'),

]
