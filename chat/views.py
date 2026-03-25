from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from .utils import get_paksiw_response
from models import WordPair

from .utils import learn_from_text, generate_markov_response

def get_paksiw_response(text):
    # 1. First, Paksiw listens and learns from the user
    learn_from_text(text)
    
    # 2. Check for your "Hardcoded" rules first (Greetings, etc.)
    if "kumusta" in text.lower():
        return "O, kumusta man ka human?"

    # 3. If no hardcoded rule, use the Markov Chain to "generate" a reply
    reply = generate_markov_response(text)
    return reply

@csrf_exempt
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

