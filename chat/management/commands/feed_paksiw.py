from django.core.management.base import BaseCommand
from chat.models import WordPair
from chat.utils import learn_from_text

class Command(BaseCommand):
    help = 'Feeds English sentences to Paksiw'

    def handle(self, *args, **kwargs):
        english_sentences = [
        # Greetings & Identity
        "Hello! How can I help you today?",
        "I am Paksiw, your friendly neighborhood AI assistant.",
        "It is a pleasure to meet you. What is on your mind?",
        "I am a digital dog with a very big brain.",
        
        # Helpfulness & Tasks
        "I can help you organize your tasks and schedule.",
        "Do you need assistance with your Django project?",
        "I am here to make your life easier and more fun.",
        "Tell me what you need, and I will try my best to help.",
        "Would you like me to create a new reminder for you?",
        
        # Conversational Fillers
        "That sounds like a great idea!",
        "I completely agree with you on that point.",
        "I am not quite sure, but I can certainly find out.",
        "Tell me more about that. I am listening.",
        "That is very interesting! Please continue.",
        
        # Common Grammar Patterns (The "Connectors")
        "The quick brown fox jumps over the lazy dog.",
        "I like to eat bones and play in the park.",
        "Programming is a very useful skill to have these days.",
        "Vercel and Neon make a very powerful combination for web apps.",
        "The weather in the Philippines is usually warm and sunny.",
        "It is important to stay hydrated and get enough sleep.",
        
        # Questions & Interaction
        "What is your favorite color?",
        "Have you ever traveled to another country?",
        "Do you enjoy working on coding projects at night?",
        "Who is your favorite superhero?",
        "How was your day? I hope it was wonderful.",
        
        # Emotional Intelligence
        "I am sorry to hear that. How can I cheer you up?",
        "Congratulations on your recent success! You earned it.",
        "Do not worry, everything will turn out fine in the end.",
        "I am feeling very happy to be chatting with you.",
        "Stay positive and keep moving forward every single day."
    ]

        self.stdout.write("Feeding Paksiw...")
        for sentence in english_sentences:
            learn_from_text(sentence)
        
        self.stdout.write(self.style.SUCCESS('Successfully fed Paksiw!'))