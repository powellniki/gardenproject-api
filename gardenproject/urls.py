from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from rest_framework import routers
from gardenapi.views import register_user, login_user
from rest_framework.authtoken.views import obtain_auth_token
from gardenapi.views import Posts, Topics, Comments, Images, Profiles

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"posts", Posts, "post")
router.register(r"topics", Topics, "topic")
router.register(r"comments", Comments, "comment")
router.register(r"images", Images, "image")
router.register(r"profiles", Profiles, "profile")


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

