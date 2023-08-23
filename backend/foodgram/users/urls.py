from django.urls import include, path
from rest_framework.routers import DefaultRouter

import users.api.views

app_name = 'api'

router = DefaultRouter()
router.register('users', users.api.views.FoodgramUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
