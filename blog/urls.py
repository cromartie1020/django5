from django.urls import path 
from . import views
urlpatterns = [
    path('',views.post_list, name='post_list'),
    #path('<int:id>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail' ),
    
    
]
                        