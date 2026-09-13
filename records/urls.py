from django.urls import path,include
from .views import DoctorView,DoctorMappingView,RegisterView,LoginView,PatientRecords,PatientsDetailView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'doctors',DoctorView,basename='doctor')
router.register(r'mappings',DoctorMappingView,basename='mapping')
urlpatterns = [
    path('',include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('patients/', PatientRecords.as_view(), name='patient_list_create'),
    path('patients/<int:pk>/', PatientsDetailView.as_view(), name='patient_detail'),
]