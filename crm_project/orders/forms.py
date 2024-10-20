from django import forms
from .models import Order, Message

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
class ManagerOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['manager','category', 'status']