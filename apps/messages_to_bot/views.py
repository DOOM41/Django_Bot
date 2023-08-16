from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from auths.models import CustomUser
from messages_to_bot.forms import SendMessageForm
from messages_to_bot.models import MessagesToBot
from messages_to_bot.utils import send_telegram_message

import asyncio

class MessageView(FormView):
    template_name: str = 'core/home.html'
    form_class = SendMessageForm
    success_url = reverse_lazy("home")

    def form_valid(self, form) -> HttpResponse:
        text = form.cleaned_data.get('text')
        user: CustomUser = self.request.user
        message = MessagesToBot.objects.create(
            user=user, 
            text_of_message=text
        )
        result_text = f"{user.first_name}, я получил от тебя сообщение:\n{text}"
        asyncio.run(send_telegram_message(
            chat_id=int(user.chat_id),
            text=result_text
        ))
        
        return super().form_valid(form)