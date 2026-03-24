from django.contrib import admin
from .models import Knowledge, ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message', 'paksiw_response', 'is_manual_reply', 'timestamp')
    list_filter = ('is_manual_reply', 'timestamp')
    search_fields = ('user_message', 'user__username')

    # Kani nga feature mo-allow nimo sa pag-reply diretso sa admin
    def save_model(self, request, obj, form, change):
        if change and obj.paksiw_response:  # Kung gi-edit nimo ang response
            obj.is_manual_reply = True
        super().save_model(request, obj, form, change)

@admin.register(Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ('keyword',)
    search_fields = ('keyword',)
