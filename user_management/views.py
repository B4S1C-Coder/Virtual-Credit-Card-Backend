from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import AdditionalUserInformation
from .serializers import (
	UserSerializer, AdditionalUserInformationSerializer
)

class LoginView(KnoxLoginView):
	authentication_classes = [BasicAuthentication]

class UserListView(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def perform_create(self, serializer):
		user_serializer = self.serializer_class(data=self.request.data)

		if user_serializer.is_valid():
			password = user_serializer.validated_data.get('password')
			user_serializer.validated_data['password'] = make_password(password)
			if user_serializer.is_valid():
				user = user_serializer.save()
				additional_info = AdditionalUserInformation.objects.create(user=user)
				serializer.instance = user

class GetAdditionalUserInformation(APIView):
	authentication_classes = [TokenAuthentication,]
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, format=None):
		try:
			user_profile = AdditionalUserInformation.objects.get(user_id=self.request.user.id)
			serializer = AdditionalUserInformationSerializer(user_profile)
			return Response(serializer.data, status.HTTP_200_OK)
		except AdditionalUserInformation.DoesNotExist:
			response = {
				"message": "profile not found",
				"userid": self.request.user.id,
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)

class UpdateUserProfilePhoto(APIView):
	authentication_classes = [TokenAuthentication,]
	permission_classes = [permissions.IsAuthenticated]
	parser_classes = [MultiPartParser,]

	def put(self, request, filename, format=None):
		file_obj = request.data['file']
		try:
			user_profile = AdditionalUserInformation.objects.get(user_id=self.request.user.id)
			user_profile.avatar = file_obj
			user_profile.save()
			return Response({
				"message": "Profile photo updated successfully.",
			}, status=status.HTTP_200_OK)
		except AdditionalUserInformation.DoesNotExist:
			return Response({
					"message": "profile not found",
					"userid": self.request.user.id,
				}, status=status.HTTP_404_NOT_FOUND)


class UserDetailView(generics.RetrieveAPIView):
	authentication_classes = [TokenAuthentication,]
	permission_classes = [permissions.IsAuthenticated,]
	queryset = User.objects.all()
	serializer_class = UserSerializer

class AdditionalUserInformationDetailView(generics.RetrieveAPIView):
	authentication_classes = [TokenAuthentication,]
	permission_classes = [permissions.IsAuthenticated,]
	queryset = AdditionalUserInformation.objects.all()
	serializer_class = AdditionalUserInformationSerializer