from django.urls import path
from rest_framework.authtoken import views  # Import for token login view

from insta_app.views.user import CreateUser, LoginUserView, RetrieveUser, UpdateUser, DestroyUser
from insta_app.views.post import CommentPost, CreatePost, DestroyPost, FollowUser, RetrievePost, RetrieveUserPosts, UpdatePost, LikePost


urlpatterns = [
    path('user/create/', CreateUser.as_view(), name='create-user'),
    path('user/login/', LoginUserView.as_view(), name='login'),
    path('user/<int:pk>/', RetrieveUser.as_view(), name='user-detail'),
    path('user/update/', UpdateUser.as_view(), name='update-user'),
    path('user/delete/<int:pk>/', DestroyUser.as_view(), name='delete-user'),
    
    path('posts/', RetrieveUserPosts.as_view(), name='user-posts'),
    path('post/create/', CreatePost.as_view(), name='create-post'),
    path('post/<int:pk>/', RetrievePost.as_view(), name='get-post'),
    path('post/update/<int:pk>/', UpdatePost.as_view(), name='update-post'),
    path('post/delete/<int:pk>/', DestroyPost.as_view(), name='delete-post'),
    
    path('post/like/<int:pk>/', LikePost.as_view(), name='like-post'),
    path('post/comments/<int:pk>/', CommentPost.as_view(), name='get-comments'),  # Assuming retrieval is implemented
    
    path('user/follow/<int:pk>/', FollowUser.as_view(), name='follow-user'),
]

