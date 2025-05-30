from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import TelegramUser
from django.conf import settings

def mini_app_first(request):
    """Render the main Mini App interface"""
    return render(request, 'second.html')

def mini_app(request):
    """Render the main Mini App interface"""
    return render(request, 'index.html')

@csrf_exempt
def mini_app_auth(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            username = data.get('username')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            # phone_number is not available from Telegram WebApp, only if previously shared
            phone_number = data.get('phone_number')  # fallback if sent
            is_admin = str(user_id) == str(settings.TELEGRAM_ADMIN_ID)

            if not user_id or not first_name:
                return JsonResponse({'status': 'error', 'message': 'User ID and first name required'}, status=400)

            user, created = TelegramUser.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'is_admin': is_admin
                }
            )
            # If user exists, update info (except phone unless provided)
            if not created:
                updated = False
                if user.username != username:
                    user.username = username
                    updated = True
                if user.first_name != first_name:
                    user.first_name = first_name
                    updated = True
                if user.last_name != last_name:
                    user.last_name = last_name
                    updated = True
                if phone_number and user.phone_number != phone_number:
                    user.phone_number = phone_number
                    updated = True
                if user.is_admin != is_admin:
                    user.is_admin = is_admin
                    updated = True
                if updated:
                    user.save()

            return JsonResponse({
                'status': 'success',
                'user': {
                    'id': user.user_id,
                    'username': user.username or 'N/A',
                    'first_name': user.first_name,
                    'last_name': user.last_name or 'N/A',
                    'phone_number': user.phone_number or 'N/A',
                    'is_admin': user.is_admin
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def second_page(request):
    return render(request, 'second.html')