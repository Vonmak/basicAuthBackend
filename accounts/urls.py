from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('profile',views.ProfileViewset, basename='profile')

urlpatterns = [
    path('signup/',views.CreateUserView.as_view(),name='signup'),
    path('login/',views.LoginView.as_view(),name='login'),
    # path('profile/', views.ProfileViewset.as_view(), name='profile'),
    # path('profile/<int:id>/', views.ProfileViewset.as_view(), name='profile_update')
]
urlpatterns += router.urls
