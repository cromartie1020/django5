from django.urls import path 
from . import views
urlpatterns = [
    path('',views.post_list, name='post_list'),
    #path('<int:id>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail' ),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment' ),
    path('post_update/<int:id>/', views.post_update, name='post_update'),
    path('post_new/', views.post_new, name='post_new'),
]
                        