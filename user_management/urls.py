from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from knox import views as knox_views
from . import views

urlpatterns = [
	path('', views.UserListView.as_view(), name="user-list"),
	path('detail/<str:pk>', views.UserDetailView.as_view(),
		name="user-detail"),
	path('more-info/<str:pk>',
		views.AdditionalUserInformationDetailView.as_view(), name="more-info"),
	path('login/', views.LoginView.as_view(), name='knox_login'),
	path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
	path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
	path('user-info/', views.GetAdditionalUserInformation.as_view(), name='user-info'),
	re_path(r'^update-profile-photo/(?P<filename>[^/]+)$',
						views.UpdateUserProfilePhoto.as_view(), name="update-profile"),
]