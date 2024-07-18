from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from gardenapi.views import register_user, login_user
from gardenapi.views import Posts

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"posts", Posts, "post")

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user)
]

