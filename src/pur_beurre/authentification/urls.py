from django.urls import path
from . import views

app_name = 'authentification'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', views.UserProfile.as_view(),
         name='profile'),
]
