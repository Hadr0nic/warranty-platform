from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from repairs.views import repair_create
from accounts.views import (
    token_login,
    #token_login_form,
    request_login,
    dashboard,
)
from comments.views import comment_create_view
from accounts.views import request_password_reset, reset_password


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/token-login/<token>/", token_login, name="token_login"),

    # Combined login page (password + email/SMS token)
    path("accounts/login/", request_login, name="login"),


    path("", repair_create, name="repair_create"),
    
    path("login/", request_login, name="login"),


    path("accounts/request-password-reset/", request_password_reset, name="request_password_reset"),
    path("accounts/reset-password/<str:token>/", reset_password, name="reset_password"),


    
    path("signup/", auth_views.LoginView.as_view(template_name="auth/signup.html"), name="signup"),
    
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout"
    ),

    path("dashboard/", dashboard, name="dashboard"),
    path(
        "create/<int:repair_id>/",
        comment_create_view,
        name="comment_create"
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
