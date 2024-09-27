from django.contrib import admin
from django.urls import path
from app.views import (
    ReactView,
    detect_disease,
    recommend_medicine,
    register_user,
    login_user,
    UserListView,
    chatbot_response,
    check_email,
    
    
)

urlpatterns = [
    path('', ReactView.as_view(), name='react-view'),  # Serve the React App
    path('api/detect-disease/', detect_disease, name='detect-disease'),  # API endpoint for disease detection
    path('api/recommend-medicine/', recommend_medicine, name='recommend-medicine'), 
    path('api/register/', register_user, name='register-user'),  # User registration
    path('api/login/', login_user, name='login-user'), 
    path('api/users/', UserListView.as_view(), name='user-list'),  # User list endpoint
    path('admin/', admin.site.urls),
    path('api/check-email/', check_email, name='check_email'),
    path('api/v1/detect-disease/', detect_disease, name='detect-disease'),



]




