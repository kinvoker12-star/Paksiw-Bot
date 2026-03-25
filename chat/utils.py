import random
import re
from .models import Knowledge, WordPair

def learn_from_text(text):
    # Clean the text and split into words
    words = re.findall(r'\b\w+\b', text.lower())  # Better word split
    if len(words) < 3:
        return

    for i in range(len(words) - 2):
        w1 = words[i]
        w2 = words[i+1]
        w3 = words[i+2]
        
        # Save trigram: w1 w2 -> w3
        pair, created = WordPair.objects.get_or_create(
            first_word=w1, 
            second_word=w2
        )
        if created:
            pair.third_word = w3
        pair.frequency += 1
        pair.save()

def generate_markov_response(seed_text):
    words = re.findall(r'\b\w+\b', seed_text.lower())
    if not words:
        return "Unsay pasabot nimo boss?"
        
    # Start with last 2 words from seed or random pair
    if len(words) >= 2:
        current_w1, current_w2 = words[-2], words[-1]
    else:
        # Fallback to any pair
        pair = WordPair.objects.first()
        if not pair:
            return "Wala pa koy enough training data. Chat more!"
        current_w1, current_w2 = pair.first_word, pair.second_word
        
    sentence = [current_w1.capitalize(), current_w2]

    # Generate chain
    for _ in range(12):  # Longer sentences
        options = WordPair.objects.filter(
            first_word=current_w1,
            second_word=current_w2
        )
        if not options.exists():
            break
            
        next_pair = options.first()  # Most frequent implicit via last learned
        next_word = next_pair.third_word
        sentence.append(next_word)
        
        # Shift window
        current_w1, current_w2 = current_w2, next_word
        
    return ' '.join(sentence) + '.'

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
            "I am not the brightest bot out there.",
            "Yes, I know that TT.",
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
