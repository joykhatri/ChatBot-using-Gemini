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
