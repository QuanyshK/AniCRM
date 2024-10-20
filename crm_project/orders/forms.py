from django import forms

from .models import Order, Message, User

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
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['manager'].queryset = User.objects.filter(is_manager=True)