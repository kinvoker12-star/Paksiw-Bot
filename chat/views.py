from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import ChatMessage
from .utils import get_paksiw_response

def chat_home(request):
    return render(request, 'chat/index.html')

def paksiw_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "")

        ai_reply = get_paksiw_response(user_input)

        ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            user_message=user_input,
            paksiw_response=ai_reply
        )

        return JsonResponse({"reply": ai_reply})

