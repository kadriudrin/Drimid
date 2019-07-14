from django.urls import path, include, re_path
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^(?P<sort_type>[\w]+)?$', views.Index.as_view(), name='index'),
    path('detail/<int:pk>', views.Detail.as_view(), name='detail'),
    path('submit', views.SubmitPost.as_view(), name='submit_post'),
    path('<int:id>/comment', views.comment, name='comment'),
    path('', include('django.contrib.auth.urls')),
    path('register', views.RegisterView.as_view(), name='register'),
    path('delete/<int:pk>', views.PostDelete.as_view(), name='post_delete'),
    path('delete/<int:post_id>/<int:pk>', views.CommentDelete.as_view(), name='comment_delete'),
    path('up_vote/<int:post_id>/<slug:nxt>', views.up_vote_post, name='up_vote_post'),
    path('down_vote/<int:post_id>/<slug:nxt>', views.down_vote_post, name='down_vote_post'),
]
