from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.utils import timezone
from datetime import timedelta
from .models import User
from repairs.models import RepairRequest
from .helpers import send_email_token, send_sms_token, TOKEN_SALT, send_password_reset_email, PASSWORD_RESET_SALT

# Dashboard
@login_required
def dashboard(request):
    repairs = RepairRequest.objects.filter(user=request.user)
    return render(request, "dashboard/dashboard.html", {"repairs": repairs})


# Token login
TOKEN_MAX_AGE = 300  # 5 minutes

def token_login(request, token):
    import urllib.parse
    token = urllib.parse.unquote(token)  # decode token from URL

    try:
        data = signing.loads(token, salt=TOKEN_SALT, max_age=TOKEN_MAX_AGE)
    except signing.SignatureExpired:
        return render(request, "accounts/token_expired.html")
    except signing.BadSignature:
        return render(request, "accounts/token_invalid.html")

    # Prevent reuse of token
    used_tokens = request.session.get("used_email_tokens", [])
    if token in used_tokens:
        return render(request, "accounts/token_invalid.html")
    used_tokens.append(token)
    request.session["used_email_tokens"] = used_tokens

    # Login user
    user = User.objects.get(id=data["user_id"])
    login(request, user)
    return redirect("dashboard")


# Combined login (password + token)
def request_login(request):
    """
    Single login page:
      - Password login if 'method' == 'password'
      - Token login via email or SMS if 'method' == 'email' or 'sms'
    """
    if request.user.is_authenticated:
        return redirect("dashboard")  # Already logged in

    if request.method == "POST":
        method = request.POST.get("method", "email")

        if method == "password":
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()

            user_auth = authenticate(request, username=username, password=password)
            if user_auth:
                login(request, user_auth)
                messages.success(request, "Logged in successfully.")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("login")

        else:
            identifier = request.POST.get("identifier", "").strip()
            try:
                if "@" in identifier:
                    user = User.objects.get(email=identifier)
                else:
                    user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                messages.error(request, "User not found")
                return redirect("login")

            if method == "email":
                send_email_token(user)
                messages.success(request, "Login token sent to your email.")
            else:  # sms
                token = send_sms_token(user, user.phone)
                request.session["sms_login_token"] = token
                messages.success(request, "Login token sent via SMS.")

            return redirect("login")

    return render(request, "accounts/login.html")



from .helpers import token_to_sms_code


def verify_sms_code(request):
    if request.method == "POST":
        entered_code = request.POST.get("code", "").strip().upper()
        token = request.session.get("sms_login_token")
        token_used = request.session.get("sms_login_token_used", False)

        if not token or token_used:
            return render(request, "accounts/token_invalid.html")

        if entered_code != token_to_sms_code(token):
            return render(request, "accounts/token_invalid.html")

        # mark as used
        request.session["sms_login_token_used"] = True

        try:
            data = signing.loads(
                token,
                TOKEN_SALT,
                max_age=TOKEN_MAX_AGE,
            )
        except signing.SignatureExpired:
            return render(request, "accounts/token_expired.html")
        except signing.BadSignature:
            return render(request, "accounts/token_invalid.html")

        if data["purpose"] != "login":
            return render(request, "accounts/token_invalid.html")

        user = User.objects.get(id=data["user_id"])
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        # optional: delete token after login
        request.session.pop("sms_login_token", None)
        request.session.pop("sms_login_token_used", None)

        return redirect("/")


from django.contrib.auth.hashers import make_password

PASSWORD_RESET_MAX_AGE = 3600  # 1 hour

# 1️1 Request password reset
def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account with this email.")
            return redirect("request_password_reset")

        send_password_reset_email(user)
        messages.success(request, "Password reset link sent to your email.")
        return redirect("login")

    return render(request, "accounts/request_password_reset.html")


# 2️2 Reset password form
def reset_password(request, token):
    import urllib.parse
    token = urllib.parse.unquote(token)

    try:
        data = signing.loads(token, salt=PASSWORD_RESET_SALT, max_age=PASSWORD_RESET_MAX_AGE)
    except signing.SignatureExpired:
        return render(request, "accounts/token_expired.html")
    except signing.BadSignature:
        return render(request, "accounts/token_invalid.html")

    if request.method == "POST":
        new_password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(request.path)

        user = User.objects.get(id=data["user_id"])
        user.password = make_password(new_password)
        user.save()
        messages.success(request, "Password reset successfully. You can login now.")
        return redirect("login")

    return render(request, "accounts/reset_password.html", {"token": token})
