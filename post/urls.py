from . import views
from django.urls import path 

urlpatterns = [
    path('' ,views.index , name= 'index'),
    path('home/', views.home , name ='home' ),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('edit/<int:pk>',views.edit,name='edit'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('logout/',views.user_logout,name='logout'),
]