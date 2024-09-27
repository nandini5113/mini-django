import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics
import ast
from rest_framework.permissions import IsAuthenticated
from .serializer import UserSerializer

class ReactView(View):
    def get(self, request):
        return JsonResponse({"message": "React View is working"})

# Load the dataset from your Desktop
data_path = r'C:\Users\TR67\OneDrive\Desktop\dataset.csv'
medication_path = r'C:\Users\TR67\OneDrive\Desktop\medication.csv'

# Load datasets
data = pd.read_csv(data_path)
medications = pd.read_csv(medication_path)

# Preprocess the dataset to create a symptom-disease mapping
symptom_disease_map = {}
disease_medicine_map = {}

# Iterate over each row in the symptom dataset
for _, row in data.iterrows():
    disease = row['Disease'].strip().lower()  # Normalize disease name
    symptoms = [str(row[f'Symptom_{i}']).strip().lower() for i in range(1, 18) if pd.notna(row[f'Symptom_{i}'])]
    if disease not in symptom_disease_map:
        symptom_disease_map[disease] = set()
    symptom_disease_map[disease].update(symptoms)

# Iterate over each row in the medication dataset
for _, row in medications.iterrows():
    disease = row['Disease'].strip().lower()  # Normalize disease name
    if 'Medicine' in row:
        medicine_str = row['Medicine']
        try:
            medicine_list = ast.literal_eval(medicine_str)
        except (ValueError, SyntaxError):
            medicine_list = ['No medicine found']
        disease_medicine_map[disease] = [med.strip().lower() for med in medicine_list]

@api_view(['POST'])
def detect_disease(request):
    symptoms = request.data.get('symptoms', [])
    symptoms = [symptom.strip().lower() for symptom in symptoms]

    detected_disease = "Unknown Disease"
    max_match_count = 0

    for disease, disease_symptoms in symptom_disease_map.items():
        match_count = len(set(symptoms).intersection(disease_symptoms))
        if match_count > max_match_count:
            max_match_count = match_count
            detected_disease = disease

    return Response({'disease': detected_disease}, status=status.HTTP_200_OK)
        


@api_view(['POST'])
def recommend_medicine(request):
    disease = request.data.get('disease', "").strip().lower()
    medicine_list = disease_medicine_map.get(disease, ["No medicine found"])
    medicine = ', '.join(medicine_list)

    return JsonResponse({'medicine': medicine}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def check_email(request):
    email = request.data.get('email')
    exists = User.objects.filter(email=email).exists()
    return Response({'exists': exists})

@api_view(['POST'])
def login_user(request):
    identifier = request.data.get('username')  
    password = request.data.get('password')

    user = authenticate(request, username=identifier, password=password)
    if user is None:
        try:
            user = User.objects.get(email=identifier)
            if user.check_password(password):
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

    if user is not None:
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
def chatbot_response(request):
    user_message = request.data.get('message', '')

    # Example logic to match the message to some predefined response
    if 'hello' in user_message:
        bot_message = 'Hello! How can I assist you today?'
    elif 'how can i detect a disease' in user_message:
        bot_message = 'You can input your symptoms, and I will help you detect the disease.'
    elif 'how do i register' in user_message:
        bot_message = 'Click on the "Login/Signup" button and follow the steps to register.'
    elif 'what is this website about' in user_message:
        bot_message = 'This website helps in disease detection based on symptoms and provides medicine recommendations.'
    elif 'can you recommend a hospital' in user_message:
        bot_message = 'Yes, I can recommend hospitals nearby based on your location.'
    elif 'thank you' in user_message:
        bot_message = 'You are welcome!'
    else:
        bot_message = 'Sorry, I did not understand that.'

    return Response({'response': bot_message})
