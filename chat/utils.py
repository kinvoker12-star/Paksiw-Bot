import random
import re
from django.db import models
from .models import Knowledge
import random
from .models import WordPair

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

def generate_markov_response(seed_text):
    words = seed_text.lower().split()
    if not words:
        return "Unsay pasabot nimo boss?"
        
    current_word = random.choice(words)
    sentence = [current_word.capitalize()]

    # Try to build a 10-word sentence
    for _ in range(10):
        options = WordPair.objects.filter(first_word=current_word)
        if not options.exists():
            break
            
        # Pick the next word based on what Paksiw has seen most often
        next_pair = random.choice(options) 
        current_word = next_pair.second_word
        sentence.append(current_word)
        
    return " ".join(sentence) + "."

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

    if any(word in text for word in ["sorry", "pasensiya",]):
        responses = [
            "I'm sorry, I didn't mean to hurt you.",
            "I'm sorry for hurting you",
        ]
        return random.choice(responses)
        
    
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
    
    if "love"   in text:
        responses = [
            "Love is a beautiful thing! It's great to feel loved and to love others.",
            "Love can be complicated, but it's also one of the most rewarding experiences in life.",
            "Love is a powerful emotion that can bring people together and create strong bonds.",
            "Love is not just a feeling, it's also an action. Show love to those around you!"
        ]
        return random.choice(responses)

    if "dionise" in text:
        responses = [
            "is Stupid.",
            "A word for stupid.",
            "That's the word for stupid!, I know that!",
        ]
        return random.choice(responses)

    if "good morning" in text:
        responses = [
            "Good morning!",
        ]
        return random.choice(responses)

    if "raymond" in text:
        responses = [
            "is Dumb.",
            "A word for dumb.",
            "That's the word for dumb!, I know that one!",
        ]
        return random.choice(response)
    
    if any(word in text for word in ["mangutana", "ngutana", "ask ko", "gi ingani", "nganong na buhat"]):
        responses = [
            "You can ask me anything you want, I'm here to help!",
            "Feel free to ask me anything, I'm here to assist you!",
            "Ask away! I'm here to provide you with information and support.",
            "Please do!",
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
    
    if any(word in text for word in ["ask", "ngutana", "mangutana", "pangutana",]):
        responses = [
            "Pangutana lang boss, Unsa man?",
            "Unsa may pangutana nimo?",
            "Ask lang",
        ]
        return random.choice(responses)
    
    if any(word in text for word in ["gwapa ko", "Am I beautiful", "I am beautiful", "gwapa ba ko",]):
        responses = [
            "Wala man koy mata to discern ug unsa ka ka gwapa, pero I'm sure you're beautiful!",
            "I know my maker so well that I can say with certainty that you are beautiful.",
            "I may be a bot, but I can still recognize beauty, and you are beautiful!",
            "As a bot, I don't have the ability to see, but based on what I know about you, I can confidently say that you are beautiful!"
        ]
        return random.choice(responses)
    
    if any(word in text for word in ["bati kog nawng", "maot ko", "am i ugly", "ugly ko", "bati ba ko", "ugly ba ko", "lain ba kog nawng",]):
        responses = [
            "Kanang mga nag ingon nimog bati, maypa e donate na nila ilang eye sight kay murag naay problema ilang mata, kay kung unsa may nakita nila, opposite gyud na sa tinuod. You're beautiful inside and out!",
            "There's no way you could be ugly, because you are a creation of someone who loves you. You're beautiful!",
            "My creator says alot about you, but one thing nga wala niya na ingon sa ako was that you're ugly.",
            "If maot ka, then there's no such thing as beauty in this world."
        ]
        return random.choice(responses)
    
    if any(word in text for word in ["char", "sure uy", "flattery", "liar", "botbot", "not true", "dili tinood",]):
        responses = [
            "I'm just being honest! I may be a bot, but I can still recognize beauty.",
            "For real!!!!",
            "Walay char char or unsan pana, sa tinood ra ta",
            "Tinuoray lang, Gwapa bitaw kaayo ka, BUYAG!! is what my creator teach me when complimenting someone"
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

    return "I don't know ug unsaon pag respond ana, I wasn't that high of a bot. " \
    "I lack a lot but I can learn!. If you just copy exacly this, kani gyud na specific line hehe: 'learn [word] is [response]'."
