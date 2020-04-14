from django.urls import path

from .views import index, by_typ

from .views import StonesCreateView

urlpatterns = [
    path('add/', StonesCreateView.as_view(), name='add'),
    path('<int:typ_id>/', by_typ, name="by_typ"),
    path('', index, name="index"),
]
