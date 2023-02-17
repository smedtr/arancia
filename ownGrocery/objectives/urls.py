from django.urls import path

from .views import objective_view,objective_list_view, index

urlpatterns = [
    path('', index, name='index'),
    # http://127.0.0.1:8000/objectives/detail_a
    path('detail_a', objective_view, name="detail_a"),
    path('list_a', objective_list_view, name="listObjectives_a"), 

]

