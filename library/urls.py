from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('authors/', views.author_list, name='author_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    # path('', views.home, name='home'),
    
    path('update_book/<int:book_id>/', views.update_book, name='update_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]
