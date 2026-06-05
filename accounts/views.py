import json
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .forms import LoginForm, RegistrationForm


def _parse_request_body(request):
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body.decode('utf-8'))
        except (ValueError, TypeError):
            return {}
    return request.POST.dict()


def _json_error_response(form, status=400):
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=status)


@ensure_csrf_cookie
@require_GET
def home_redirect(request):
    return redirect('accounts:login_page')


@ensure_csrf_cookie
@require_GET
def login_page_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_page')
    return render(request, 'login.html')


@ensure_csrf_cookie
@require_GET
def register_page_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_page')
    return render(request, 'register.html')


@login_required
@require_GET
def dashboard_page_view(request):
    return render(request, 'dashboard.html')


@csrf_protect
@require_POST
def register_view(request):
    payload = _parse_request_body(request)
    form = RegistrationForm(payload)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Account created successfully.'}, status=201)
    return _json_error_response(form)


@csrf_protect
@require_POST
def login_view(request):
    payload = _parse_request_body(request)
    form = LoginForm(payload)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return JsonResponse({
            'status': 'success',
            'message': 'Login successful.',
            'user': {
                'username': user.username,
                'email': user.email,
            },
        })
    return _json_error_response(form)


@csrf_protect
@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'Logout completed successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Authentication required.'}, status=401)


@require_GET
def dashboard_api_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required.'}, status=401)
    return JsonResponse({
        'status': 'success',
        'dashboard': {
            'username': request.user.username,
            'email': request.user.email,
            'message': 'Authenticated dashboard access granted.',
        },
    })


@ensure_csrf_cookie
@require_GET
def csrf_token_view(request):
    return JsonResponse({
        'status': 'success',
        'csrfToken': get_token(request),
        'message': 'CSRF cookie has been set.',
    })
