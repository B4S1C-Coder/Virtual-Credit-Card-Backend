from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.CreditCardView.as_view(), name='credit-card'),
	re_path(r'^create/(?P<filename>[^/]+)$', views.CreateCreditCardView.as_view(), name="createcard")
]