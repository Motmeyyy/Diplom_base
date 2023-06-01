from django.contrib import admin
from .models import Post
from users.models import VerificationRequest
admin.site.register(Post)
admin.site.register(VerificationRequest)