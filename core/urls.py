from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),

    # Patient
    path('patient/register/', views.patient_register, name='patient_register'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    # Doctor
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('doctor/register/', views.doctor_register, name='doctor_register'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

    # API
    path('api/search-patient/', views.search_patient, name='search_patient'),
    path('api/simulate-access/', views.simulate_access, name='simulate_access'),
    path('api/add-visit/', views.add_visit, name='add_visit'),

    path('logout/', views.logout_view, name='logout'),
]
