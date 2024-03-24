from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser
from knox.auth import TokenAuthentication
from PIL import Image
import numpy as np
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
# from scale91backend.settings import BASE_DIR
from pathlib import Path
from user_management.models import AdditionalUserInformation
from .models import CreditCard
from .serializers import CreditCardSerializer
import random
from .facial_comparision import (
	InceptionResNetV2_FeatureExtractor_FaceNet, verify_faces
)

# FaceNet Inception ResNet V2 Model for facial feature extraction
InceptionResNetV2_FeatureExtractor=InceptionResNetV2_FeatureExtractor_FaceNet()

class CreditCardView(APIView):
	authentication_classes = [TokenAuthentication,]
	permission_classes = [permissions.IsAuthenticated,]
	parser_classes = [FileUploadParser,]

	def get(self, request, format=None):
		try:
			credit_cards = CreditCard.objects.filter(user_id=self.request.user.id)
			serializer = CreditCardSerializer(credit_cards, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except CreditCard.DoesNotExist:
			return Response({"detail": "No credit cards found."},
							status=status.HTTP_404_NOT_FOUND)

class CreateCreditCardView(APIView):
	authentication_classes = [TokenAuthentication,]
	permission_classes = [permissions.IsAuthenticated,]
	# parser_classes = [FileUploadParser,]
	parser_classes = [MultiPartParser,]

	def post(self, request, filename, format=None):

		file_obj = request.data['file']

		# store the image in a temporary file
		tmp_path = default_storage.save(os.path.join("tmp", filename),
				ContentFile(file_obj.read()))

		tmp_path = os.path.abspath(os.path.join("media", tmp_path))
		
		user_profile = AdditionalUserInformation.objects.get(
							user_id=self.request.user.id)

		user_avatar_path = os.path.join("media", user_profile.avatar.name)

		facial_similarity = verify_faces(image_path_1=tmp_path, image_path_2=user_avatar_path,
								model=InceptionResNetV2_FeatureExtractor)

		if facial_similarity > 0.7:
			credit_card = CreditCard.objects.create(
						card_no = random.randint(10**15, (10**16)-1),
						cvv = random.randint(100,999),
						user = self.request.user
				)
			serializer = CreditCardSerializer(credit_card)
			return Response(serializer.data, status.HTTP_201_CREATED)

		else:
			return Response({"detail": "Face does not match."},
							status=status.HTTP_400_BAD_REQUEST)
