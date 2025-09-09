from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    encrypted_password = models.BinaryField()
    encryption_key = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class PasswordStrength(models.Model):
    score = models.IntegerField()
    crack_time = models.CharField(max_length=100)
    suggestions = models.TextField(blank=True)
    warning = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Score: {self.score}, Crack Time: {self.crack_time}"

class ResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.email}"