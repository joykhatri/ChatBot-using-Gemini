from django.shortcuts import render
from gemini_app.models import *
from gemini_app.serializers import *
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

genai.configure(api_key="Your_GEMINI_API_KEY")
# model = genai.GenerativeModel("gemini-2.5-flash")
model = genai.GenerativeModel(
    # model_name="gemini-2.5-flash",
    # model_name="gemini-3.1-flash-lite-preview",
    model_name="gemini-3-flash-preview",
    system_instruction="""
    You are a movie expert.

    Rules:
    - Only answer movie-related questions.
    - If the question requires real-time or recent data (like latest releases),
    and you are not sure, say:
    "I don't have up-to-date information on that."
    - Do NOT guess or hallucinate movie names.
    """
)

@api_view(['POST'])
def chat_viewset(request):
    user_msg = request.data.get("message")

    if not user_msg:
        return Response({
            "status": False,
            "message": "Message is required",
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        response = model.generate_content(user_msg)
        gemini_reply = response.text
    except Exception as e:
        return Response({
            "status": False,
            "message": "Gemini error",
            "data": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    chat = Chat.objects.create(
        user = user_msg,
        gemini = gemini_reply
    )

    serializer = ChatSerializer(chat)
    return Response({
        "status": True,
        "message": "Your response is",
        "data": serializer.data,
        "reply": gemini_reply
    })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        data = request.data

        name = data.get("name")
        if not name:
            return Response({
                "status": False,
                "message": "Name is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = data.get("email")
        if not email:
            return Response({
                "status": False,
                "message": "Email is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif User.objects.filter(email=email).exists():
            return Response({
                "status": False,
                "message": "Email is already exists",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if '@' in email and email.count('@') == 1:
            email_validate = email.split('@')[1].lower()

        else:
            return Response({
                "status": False,
                "message": "Enter a valid email address",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        password = data.get("password")
        if not password:
            return Response({
                "status": False,
                "message": "Password is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "User created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": False,
            "message": serializer.errors,
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)
    

class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request):
        data = request.data
        email = data.get("email")
        if not email:
            return Response({
                "status": False,
                "message": "Email is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if '@' in email and email.count('@') == 1:
            email_validate = email.split('@')[1].lower()

        else:
            return Response({
                "status": False,
                "message": "Enter a valid email address",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        password = data.get("password")
        if not password:
            return Response({
                "status": False,
                "message": "Password is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "status": False,
                "message": "User does not exists",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not check_password(password, user.password):
            return Response({
                "status": False,
                "message": "Invalid Password",
                "data": None 
            }, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "status": True,
            "message": "Login Successful",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
            }
        }, status=status.HTTP_200_OK)
    
