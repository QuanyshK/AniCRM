from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Order(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='managed_orders', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    order = models.ForeignKey(Order, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender} in {self.order.title}"
