from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('create-post', views.createpost, name='create-post'),
    path('profile/<str:user_id>', views.profile, name='profile'),
    path('post_page/<str:post_id>', views.post_page, name='post_page')
]
