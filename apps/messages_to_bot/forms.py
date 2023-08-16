from django import forms


class SendMessageForm(forms.Form):
    text = forms.CharField(
        widget=forms.TextInput(),
        label='Введите ваше сообщение'
    )