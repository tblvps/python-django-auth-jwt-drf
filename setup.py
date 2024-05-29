import os
import subprocess

# Function to run shell commands
def run_command(command):
    subprocess.run(command, shell=True, check=True)

# Create Django project
project_name = "dev"
app_name = "at"
app_name2 = "ai"
tbl = "docs"
# Step 1: Set Up Your Django Project
print("Setting up Django project...")
run_command(f"mkdir {tbl}")
os.chdir(tbl)
run_command(f"pip install pipenv")
run_command(f"pip install pipenv")
run_command(f"pipenv install tzdata")
run_command(f"pipenv install requests-oauthlib")
run_command(f"pipenv install django")
run_command(f"django-admin startproject {project_name}")
os.chdir(project_name)
run_command(f"python manage.py startapp {app_name}")
run_command(f"python manage.py startapp {app_name2}")
# Step 2: Install and Configure Django Allauth
print("Installing Django Allauth...")
run_command("pipenv install django-allauth")

# Add Allauth configuration to settings.py
settings_path = f"{project_name}/settings.py"
with open(settings_path, 'a') as f:
    f.write("""
INSTALLED_APPS += [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.auth0',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.paypal',
    'allauth.socialaccount.providers.microsoft',
    'allauth.socialaccount.providers.twitter',
    'ai',
    'at',
]

MIDDLEWARE += [
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = '/'
""")

# Include Allauth URLs
with open(f"{project_name}/urls.py", 'w') as f:
    f.write("""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('ai', include('rest_framework.urls')),
]
""")

# Step 3: Install and Configure Tailwind CSS
print("Installing Tailwind CSS...")
run_command("npm install -D tailwindcss")
run_command("npx tailwindcss init")

# Create Tailwind config
tailwind_config = """
module.exports = {
  content: [
    './templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
with open("tailwind.config.js", 'w') as f:
    f.write(tailwind_config)

# Create Tailwind CSS file
os.makedirs("static/css", exist_ok=True)
tailwind_css = """
@tailwind base;
@tailwind components;
@tailwind utilities;
"""
with open("static/css/tailwind.css", 'w') as f:
    f.write(tailwind_css)

# Build Tailwind CSS
run_command("npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/output.css --watch &")

# Include Tailwind CSS in base template
os.makedirs("templates", exist_ok=True)
base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Site{% endblock %}</title>
    <link href="{% static 'css/output.css' %}" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <header class="p-4 bg-blue-600 text-white">
        <nav class="container mx-auto">
            <ul class="flex space-x-4">
                <li><a href="/" class="hover:underline">Home</a></li>
                {% if user.is_authenticated %}
                <li><a href="{% url 'account_logout' %}" class="hover:underline">Logout</a></li>
                {% else %}
                <li><a href="{% url 'account_login' %}" class="hover:underline">Login</a></li>
                <li><a href="{% url 'account_signup' %}" class="hover:underline">Sign up</a></li>
                {% endif %}
            </ul>
        </nav>
    </header>
    <main class="container mx-auto p-4">
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>
"""
with open("templates/base_generic.html", 'w') as f:
    f.write(base_template)

# Step 4: Create Custom Login Template
login_template = """
{% extends "base_generic.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="max-w-md mx-auto bg-white p-8 border border-gray-300 rounded">
    <h2 class="text-2xl font-bold mb-6 text-gray-900">Login</h2>
    <form method="post" action="{% url 'account_login' %}">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:bg-blue-700">
            Login
        </button>
    </form>
    <p class="mt-6 text-center">Don't have an account? <a href="{% url 'account_signup' %}" class="text-blue-600 hover:underline">Sign up</a></p>
</div>
{% endblock %}
"""
os.makedirs("templates/account", exist_ok=True)
with open("templates/account/login.html", 'w') as f:
    f.write(login_template)

# Step 5: Install and Configure Django Rest Framework and JWT Authentication
print("Installing Django Rest Framework and JWT...")
run_command("pipenv install djangorestframework")
run_command("pipenv install djangorestframework-simplejwt")

# Add DRF and JWT configuration to settings.py
with open(settings_path, 'a') as f:
    f.write("""
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    )
  }

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "VERIFIED_EMAIL": True
    },
    "google": {
        "APPS": [
            {
                "client_id": "875367988237-ialg9n0co204jvhsldo04dudj8je7s6j.apps.googleusercontent.com",
                "secret": "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",
                "key": ""
            },
        ],

        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
""")

# Include JWT authentication URLs
with open(f"{app_name}/urls.py", 'w') as f:
    f.write("""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

token = RefreshToken(base64_encoded_token_string)
token.blacklist()

urlpatterns = [
    path('ai/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('ai/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ai/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('ai/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
""")

# Step 6: Create Custom User Model
print("Creating custom user model...")
custom_user_model = """
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # change this to something unique
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Ensure this is also unique if it's not already set
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )
"""
with open(f"{app_name}/models.py", 'w') as f:
    f.write(custom_user_model)

# Update settings.py to use the custom user model

# Create and apply migrations
run_command("pipenv run python manage.py makemigrations")
run_command("pipenv run python manage.py migrate")
run_command("pipenv run python manage.py createsuperuser")
# Step 7: Create API Views
print("Creating API views...")
os.makedirs(f"{app_name2}", exist_ok=True)

serializers = """
from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
"""
with open(f"{app_name2}/serializers.py", 'w') as f:
    f.write(serializers)

views = """
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from .AI.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
"""
with open(f"{app_name2}/views.py", 'w') as f:
    f.write(views)

api_urls = """
from django.urls import include, path
from rest_framework import routers

from .AI import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ai/', include('rest_framework.urls', namespace='rest_framework'))
]
"""
with open(f"{app_name2}/urls.py", 'w') as f:
    f.write(api_urls)

# Step 8: Configure Django to Serve Static Files
with open(settings_path, 'a') as f:
    f.write("""
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
""")

# Run the development server
print("Running the development server...")
run_command("pipenv run python manage.py runserver")
