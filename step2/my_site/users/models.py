from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    full_name = models.CharField(max_length=255, default='FIO')
    polis = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    heart_rate = models.IntegerField(null=True,blank=True)
    diet = models.ForeignKey('Diet', on_delete=models.SET_NULL, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    email_key = models.CharField(max_length=255, default='Nz2cNLSLUb3UhKf6eQvb')
    email_sender = models.CharField(max_length=255, default='ivankov2001@gmail.com')

    def __str__(self):
        return f'{self.user.username} Profile'

    def __str__(self):
        if self.diet:
            return str(self.diet)
        else:
            return "Диета не выбрана"


class VerificationRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=20)


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return f"Appointment for {self.patient.username} with {self.doctor.username} at {self.date}"


class HeartRate(models.Model):
        rate = models.IntegerField()
        timestamp = models.DateTimeField(auto_now_add=True)

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    receipt_hash = models.CharField(max_length=32, unique=True)
    diet = models.ForeignKey('Diet', on_delete=models.SET_NULL, blank=True, null=True)  # Поле для связи с диетой

    def __str__(self):
        return f'{self.user.username} - {self.item}'


class Diet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    recipes = models.ManyToManyField('Recipe',blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField('Product')
    image = models.ImageField(upload_to='recipe_images', null=True, blank=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    product_norm = models.CharField(max_length=255, blank=True, null=True)
    brand_norm = models.CharField(max_length=255, blank=True, null=True)
    cat_norm = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


