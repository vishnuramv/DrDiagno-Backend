# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from tensorflow.keras.models import load_model
from django.conf import settings
import os
#import pickle
class PredictDisease(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, format=None):
		diseases = ["(vertigo) Paroymsal  Positional Vertigo", "AIDS", "Acne", "Alcoholic hepatitis", "Allergy", "Arthritis", "Bronchial Asthma", "Cervical spondylosis", "Chicken pox", "Chronic cholestasis", "Common Cold", "Dengue", "Diabetes ", "Dimorphic hemmorhoids(piles)", "Drug Reaction", "Fungal infection", "GERD", "Gastroenteritis", "Heart attack", "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E", "Hypertension ", "Hyperthyroidism", "Hypoglycemia", "Hypothyroidism", "Impetigo", "Jaundice", "Malaria", "Migraine", "Osteoarthristis", "Paralysis (brain hemorrhage)", "Peptic ulcer diseae", "Pneumonia", "Psoriasis", "Tuberculosis", "Typhoid", "Urinary tract infection", "Varicose veins", "hepatitis A"]
		modelPath = "rf.pkl"
		symptoms = [request.data.get("symptoms")]
		preditionDate = request.data.get("preditionDate")
		model = load_model(os.path.join(settings.MODEL_ROOT, modelPath))
		prediction = model.predict(symptoms)
		print(prediction)
		predictedDisease = {}
		for i in range(len(diseases)):
			predictedDisease[diseases[i]] = prediction[0][i]
		try:
			return Response({
				"msg": "Predicted successfully",
				"predictedDisease" : predictedDisease
			}, status=status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({
				"error": "Something went wrong"
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
