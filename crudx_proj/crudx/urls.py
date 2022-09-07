from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('create',views.create, name='create'),
    path('update/<int:pk>',views.update, name='update'),
    path('delete/<int:pk>',views.delete, name='delete'),
    path('crud/',views.crud, name='crud'),
    path('signup',views.signup, name='signup'),
    path('login',views.loginuser, name='login'),
    path('logout',views.logoutuser, name='logout'),
]