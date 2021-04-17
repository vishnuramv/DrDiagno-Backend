# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
#from tensorflow.keras.models import load_model
from django.conf import settings
import os
import pickle
from .models import Prediction


class PredictDisease(APIView):
#	permission_classes = (AllowAny,)
	diseases = ["(vertigo) Paroymsal  Positional Vertigo", "AIDS", "Acne", "Alcoholic hepatitis", "Allergy", "Arthritis", "Bronchial Asthma", "Cervical spondylosis", "Chicken pox", "Chronic cholestasis", "Common Cold", "Dengue", "Diabetes ", "Dimorphic hemmorhoids(piles)", "Drug Reaction", "Fungal infection", "GERD", "Gastroenteritis", "Heart attack", "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E", "Hypertension ", "Hyperthyroidism", "Hypoglycemia", "Hypothyroidism", "Impetigo", "Jaundice", "Malaria", "Migraine", "Osteoarthristis", "Paralysis (brain hemorrhage)", "Peptic ulcer diseae", "Pneumonia", "Psoriasis", "Tuberculosis", "Typhoid", "Urinary tract infection", "Varicose veins", "hepatitis A"]
	def post(self, request, format=None):
		modelPath = "rf.pkl"
		symptoms = [request.data.get("symptoms")]
		preditionDate = request.data.get("preditionDate")
		try:
			model = pickle.load(open(os.path.join(settings.MODEL_ROOT, modelPath), 'rb'))
			prediction = model.predict_proba(symptoms)
			print(prediction)
			predictedDisease = {}
			predictionString = ""
			for i in range(len(self.diseases)):
				predictedDisease[self.diseases[i]] = prediction[0][i]
				predictionString += str(prediction[0][i]) + "|"
			predictionModel = Prediction()
			predictionModel.user = request.user
			predictionModel.prediction = predictionString
			predictionModel.save()
			return Response({
				"msg": "Predicted successfully",
				"predictedDisease" : predictedDisease
			}, status=status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({
				"error": "Something went wrong"
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	def get(self, request, format=None):
		user = request.user
		previousPredictions = Prediction.objects.filter(user=user)
		returnPrediction = []
		for i in previousPredictions:
			predict = i.prediction.split('|')
			predictedDisease = {}
			for j in range(len(self.diseases)):
				predictedDisease[self.diseases[j]] = predict[j]
			returnPrediction.append({
				"date" : i.date,
				"predictedDisease" : predictedDisease
			})
		return Response({
				"msg": "Predicted successfully",
				"previousPredictions" : returnPrediction
			}, status=status.HTTP_200_OK)
			
