from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,   # POST /api/token/
    TokenRefreshView,      # POST /api/token/refresh/
    TokenVerifyView,       # POST /api/token/verify/
)
from student_records.views import StudentRecordViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'student-records', StudentRecordViewSet, basename='student-records')

urlpatterns = [
    path('admin/',                  admin.site.urls),
    path('api/token/',              TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',      TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/',       TokenVerifyView.as_view(), name='token_verify'),
    path('api/',                    include(router.urls)),
    path('api/register/',           UserRegistrationView.as_view(), name='register'),
]