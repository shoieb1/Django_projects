from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import User, PasswordStrength, ResetToken
from cryptography.fernet import Fernet
from django.core.mail import send_mail
from django.conf import settings
import json
import uuid
from datetime import datetime, timedelta

def index(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request, 'login.html')

def main_page(request):
    return render(request, 'main.html')

def forgot_password_page(request):
    return render(request, 'forgot-password.html')

def reset_password_page(request):
    return render(request, 'reset-password.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            if not email or not password:
                return JsonResponse({"message": "Please provide email and password"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email already exists"}, status=400)
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted_password = fernet.encrypt(password.encode('utf-8'))
            User.objects.create(
                email=email,
                encrypted_password=encrypted_password,
                encryption_key=key
            )
            return JsonResponse({"message": "Account created successfully"})
        except Exception as e:
            print(f"Error in register: {e}")
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            try:
                user = User.objects.get(email=email)
                fernet = Fernet(user.encryption_key)
                decrypted_password = fernet.decrypt(user.encrypted_password).decode('utf-8')
                if decrypted_password == password:
                    return JsonResponse({"message": "Login successful", "redirect": "/main.html"})
                else:
                    return JsonResponse({"message": "Invalid email or password"}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"message": "Invalid email or password"}, status=400)
        except Exception as e:
            print(f"Error in login: {e}")
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def save_strength(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            PasswordStrength.objects.create(
                score=data.get('score'),
                crack_time=data.get('crack_time'),
                suggestions=data.get('suggestions', ''),
                warning=data.get('warning', '')
            )
            return JsonResponse({"message": "Strength saved successfully"})
        except Exception as e:
            print(f"Error in save_strength: {e}")
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email not found"}, status=400)
            # Generate a 6-digit verification code
            code = str(uuid.uuid4())[:6]
            expires_at = datetime.now() + timedelta(minutes=15)  # Code expires in 15 minutes
            ResetToken.objects.create(
                email=email,
                token=code,
                expires_at=expires_at
            )
            # Send email with verification code
            subject = 'Password Reset Verification Code'
            message = f'Your verification code is: {code}\n\nThis code will expire in 15 minutes.\n\nIf you did not request a password reset, please ignore this email.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return JsonResponse({"message": "Verification code sent"})
        except Exception as e:
            print(f"Error in forgot_password: {e}")
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            code = data.get('code')
            password = data.get('password')
            try:
                reset_token = ResetToken.objects.get(
                    email=email,
                    token=code,
                    used=False,
                    expires_at__gt=datetime.now()
                )
                user = User.objects.get(email=email)
                key = Fernet.generate_key()
                fernet = Fernet(key)
                encrypted_password = fernet.encrypt(password.encode('utf-8'))
                user.encrypted_password = encrypted_password
                user.encryption_key = key
                user.save()
                reset_token.used = True
                reset_token.save()
                return JsonResponse({"message": "Password reset successfully"})
            except (ResetToken.DoesNotExist, User.DoesNotExist):
                return JsonResponse({"message": "Invalid or expired verification code"}, status=400)
        except Exception as e:
            print(f"Error in reset_password: {e}")
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        return JsonResponse({"message": "Logged out successfully"})
    return JsonResponse({"message": "Method not allowed"}, status=405)