from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from gardenapi.views import register_user, login_user
from rest_framework.authtoken.views import obtain_auth_token
from gardenapi.views import Posts, Topics

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"posts", Posts, "post")
router.register(r"topics", Topics, "topic")


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework"))
]

