import random
import re
from django.db import models
from .models import Knowledge

def get_paksiw_response(text):  # Renamed from process_user_input, user_id=None for now
    text = text.lower()

    # 1. KEYWORD: Greetings (Multiple Responses)
    if any(word in text for word in ["hello", "hi", "wassup", "kamusta"]):
        responses = [
            "Sup! Paksiw here. Unsay ayo?",
            "Beep boop! Ready na ko mo remind nimo.",
            "O, kumusta man ka human?"
        ]
        return random.choice(responses)
    
    if any (word in text for word in ["purpose","gamit", "exist", "made"]):
        responses = [
            "Ang akoang purpose is ang maghatag sa imohag kalingawan ug mag remind sa imohang schedule!."
            "Ni exist si Paksiw for you!"
            "I was made for you as Assistant!."
        ]
        return random.choices(responses)

    # 2. KEYWORD: Name / Identity
    if any(word in text for word in ["ngalan", "name", "kinsa"]):
        responses = [
            "Paksiw ang bangiitang irong buang!",
            "Ako si Paksiw, imong personal assistant.",
            "Secret! Joke, Paksiw ra bitaw ko."
        ]
        return random.choice(responses)

    # 3. KEYWORD: Reminders
    if any(word in text for word in ["remind", "schedule","Add task", "task"]):
        responses = [
            "Wala pa na ma implement nga function boss, I'm Sorry.",
            "Sorry gyud kaayo boss, kay bogoon man gud kaayo ning tighimo nako ga error'2 sa task! HAHAHAHAH.",
            "Sorry boss, Wala pako ana na function."
        ]
        return random.choice(responses)


    if any(word in text for word in ["love me", "love",]):
        responses = [
            "He do love you, He's just dumb maybe.",
            "He's kinda of a fool, but he does love you",
            "He love you",
            "He made me, He does :)"
        ]
        return random.choice(responses)
    
    if any(word in text for word in ["rant", "share", "ge ingani", "gi ingani", "nganong na buhat"]):
        responses = [
            "You can share anything you want diri sa akoa.",
            "Rant lang diri sa akoa, atoa pa siyang e bash HAHHAHAHAHAHA",
            "Kinsay gabuhat ani nimo?, ang ga himo sa akoa? tsk tsk tsk tung tawhana to!",
            "rant lang rant, maminaw ra ko"
        ]
        return random.choice(responses)
  

    # LEARNING MODE: "paksiw, learn [keyword] is [response]"
    learn_match = re.search(r"learn (.+) is (.+)", text)
    if learn_match:
        keyword = learn_match.group(1).strip()
        response = learn_match.group(2).strip()
        obj, created = Knowledge.objects.get_or_create(keyword=keyword)
        if created:
            obj.responses = response
        else:
            obj.responses += f"|{response}"
        obj.save()
        return f"Got it! Learned '{keyword}' -> '{response}'."

    # DYNAMIC KNOWLEDGE LOOKUP
    words = text.split()
    for word in words:
        try:
            knowledge = Knowledge.objects.filter(keyword__iexact=word).first()
            if knowledge:
                return knowledge.get_random_response()
        except:
            pass

    return "I don't know ug unsaon pag respond ana, I wasn't that high of a bot. " \
    "I lack a lot but I can learn!. If you just copy exacly this, kani gyud na specific line hehe: 'learn [word] is [response]'."
