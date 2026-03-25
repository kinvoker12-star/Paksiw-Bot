from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage, WordPair
from .utils import get_paksiw_response

def chat_home(request):
    """Render the main chat interface."""
    return render(request, 'chat/index.html')

@csrf_exempt
def paksiw_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "")

        # Learn first (no DB access needed)
        from .utils import learn_from_text
        learn_from_text(user_input)

        ai_reply = get_paksiw_response(user_input)

        ChatMessage.objects.create(
            user=None,  # Anonymous OK, nullable field
            user_message=user_input,
            paksiw_response=ai_reply
        )

        return JsonResponse({"reply": ai_reply})

