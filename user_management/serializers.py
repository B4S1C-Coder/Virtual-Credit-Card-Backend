from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AdditionalUserInformation

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ["id", "username", "email", "password"]
	# profile_id = serializers.SerializerMethodField('get_profile_id')

	# def get_profile_id(self, instance):
	# 	user_id = instance.get('id', -1)
	# 	try:
	# 		user_profile = AdditionalUserInformation.objects.get(pk=user_id)
	# 		profile_id = user_profile.id
	# 	except AdditionalUserInformation.DoesNotExist:
	# 		profile_id = -1
	# 	return profile_id

	# def create(self, validated_data):
	# 	user = User.objects.create(**validated_data)
	# 	AdditionalUserInformation.objects.create(user=user)
	# 	return user

# class NormalUsageUserSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = ["id", "username", "email"]

class AdditionalUserInformationSerializer(serializers.ModelSerializer):
	userid = serializers.ReadOnlyField(source="user.id")
	user = serializers.ReadOnlyField(source="user.username")
	email = serializers.ReadOnlyField(source="user.email")
	class Meta:
		model = AdditionalUserInformation
		fields = ["id", "user", "phone_no", "bio", "avatar", "email",
				"status", "userid"]