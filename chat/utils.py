import random
import re
from .models import Knowledge, WordPair

def learn_from_text(text):
    # Clean the text and split into words
    words = text.lower().split()
    if len(words) < 2:
        return

    for i in range(len(words) - 1):
        w1 = words[i]
        w2 = words[i+1]
        
        # Save the connection to Neon
        pair, created = WordPair.objects.get_or_create(first_word=w1, second_word=w2)
        if not created:
            pair.frequency += 1
            pair.save()

import random
from .models import WordPair

def generate_markov_response(seed_text):
    words = seed_text.lower().split()
    if not words:
        return "I'm listening. Tell me more!"
        
    # Start with a random word from the user's input
    current_word = random.choice(words)
    sentence = [current_word.capitalize()]

    for _ in range(12): # Max sentence length
        options = WordPair.objects.filter(first_word=current_word)
        
        if not options.exists():
            break
            
        # --- THE "SANE" LOGIC ---
        # 1. Get all possible next words and their frequencies
        next_words = [p.second_word for p in options]
        weights = [p.frequency for p in options]
        
        # 2. Pick the next word based on probability (higher frequency = higher chance)
        current_word = random.choices(next_words, weights=weights, k=1)[0]
        # ------------------------

        sentence.append(current_word)
        
    return " ".join(sentence) + "."

def get_paksiw_response(text):  # Renamed from process_user_input, user_id=None for now
    text = text.lower()
    

    if any(word in text for word in ["who made you", "who created you", "who is your creator"]):
        responses = [
            "I was created by ONI, a not so great programmer, but he made me for you!",
            "ONI is the one who made me, he's not the best coder but he did his best to make me for you!",
            "My creator is ONI, he's not the best programmer but he made me for you!",
            "Oni is the one who made me!"
        ]
        return random.choice(responses)

    if any(word in text for word in ["unsa ka", "what are you", "bot ka", "ai ka"]):
        responses = [
            "I am a cheap AI chat bot that was manually coded by the hands of ONI the not so great.",
            "A cheap AI chat bot",
            "An AI chat bot that is incomplete and in a lot of development"
        ]
        return random.choice(responses)
    
    if any (word in text for word in ["purpose","gamit", "exist", " you made"]):
        responses = [
            "Ang akoang purpose is ang maghatag sa imohag kalingawan ug mag remind sa imohang schedule!.",
            "Ni exist si Paksiw for you!",
            "I was made for you as Assistant!."
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

    if any(word in text for word in ["love me", "he love",]):
        responses = [
            "He do love you, He's just dumb maybe.",
            "He's kinda of a fool, but he does love you",
            "He love you",
            "He made me, He does :)"
        ]
        return random.choice(responses)

    if any(word in text for word in ["dumb", "stupid", "idiot", "baka", "gago", "tanga","bogo"]):
        responses = [
            "I'm sorry about that hehe.",
            "I'm still on my early phase of development, but I'm learning and improving every day!",
            "I may not be the smartest bot out there, but I'm doing my best to be helpful and entertaining for you!",
            "I may be a bit slow, but I'm always here to listen and chat with you!",
            "I am not the brightest bot out there."
            "Yes, I know that TT."
            "But am I more dionise than my creator? That's a question for the ages!",
            "Yes, i'm so dionise TT.",
            "Yes yes yes, I'm dionise and raymond at the same time. I'm sorry TT.",
        ]
        return random.choice(responses)

    if "dionise" in text:
        responses = [
            "is Stupid.",
            "A word for stupid.",
            "That's the word for stupid!, I know that!",
        ]
        return random.choice(responses)

    if "raymond" in text:
        responses = [
            "is Dumb.",
            "A word for dumb.",
            "That's the word for dumb!, I know that one!",
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
    
    if any(word in text for word in ["What is buyag", "unsa manang buyag", "buyag is",]):
        responses = [
            "Cebuanos or Visayan speakers usually say this to prevent any bad thing from happening to someone when being complimented by another."
        ]
        return random.choice(responses)
    
    if any(word in text for word in ["Good bye", "goodbye", "bye",]):
        responses = [
            "Good bye boss!, See you later!",
            "Bye boss, Take care!",
            "See you later boss, Take care!"
            "Visit me again boss, I'll be here waiting for you!"
            "Come again boss, I hope i'll be upgraded by then, I want to be more useful for you!"
        ]
        return random.choice(responses)
    
    if any(word in text for word in ["I am tired", "tired", "so tired", "kapoy", "kapoy na ko", "tired na ko", "kapoy", "I wanna rest", "rest"]):
        responses = [
            "I understand how you feel, it's important to take care of yourself and get some rest when you need it.",
            "It's okay to feel tired sometimes, make sure to get enough sleep and take breaks when you can.",
            "Remember to take care of yourself and prioritize rest when you need it. Your well-being is important!",
            "Pahuway lang boss, I hope you get the rest you need to feel better soon!",
            "Masahion ta tika boss, para ma relax ka.",
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

    return generate_markov_response(text)
