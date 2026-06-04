"""
URL configuration for mangalya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from app import views
from django.conf.urls.static import static
from app.views import social_landing_slug, create_booking_lead

from django.contrib.sitemaps.views import sitemap
from app.sitemaps import StaticViewSitemap


from django.contrib.auth import views as auth_views








sitemaps = {
    'static': StaticViewSitemap
}




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('treatments',views.treatments,name='treatments'),
    path('contact-us',views.contact,name='contact'),
     path('careers/', views.careers, name='careers'),

    path('book-appointment/',views.book_appointment,name='book_appointment'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path("update-status/", views.update_visit_status, name="update_status"),


    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('homeopathic/',views.homeopathic,name='homeopathic'),
     path("sitemap.xml/", sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    #  path("patient-login/",views.patient_login,name="patient_login")

    path('social-landing/<slug:slug>/', social_landing_slug, name='social_landing_slug'),
    path('api/booking-lead/', create_booking_lead, name='create_booking_lead'),
    path("skin-treatments/",views.skin_treatments,name="skin_treatments"),

    path('get-booked-slots/', views.get_booked_slots, name='get_booked_slots'),
    path("get-holidays/", views.get_holidays, name="get_holidays"),


     path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login"
    ),

    # LOGOUT
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    path("dashboard/", views.dashboard_home, name="dashboard_home"),

    path(
    "dashboard/appointments/",
    views.dashboard_appointments,
    name="appointments"
),

# path(
#     'appointment-success/',
#     views.appointment_success,
#     name='appointment_success'
# ),


path(
    'appointment-success/<str:booking_id>/',
    views.appointment_success,
    name='appointment_success'
),

path("my-appointments/", views.my_appointments, name="my_appointments"),
path("my-appointments/verify/", views.my_appointments_verify, name="my_appointments_verify"),
path("hair-health-index/", views.hhi, name="hhi"),


path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),


path(
    'download-appointment/<str:booking_id>/',
    views.download_appointment_pdf,
    name='download_appointment'
),



# =============================== landing page =========================

path(
    'pcod-treatment-in-homeopathy/',
    views.pcodTreatment,
    name='pcod-treatment'
),

# =================================================testing

path(
    'test-booking/',
    views.test_booking
),


path(
    'test-login/',
    views.test_login,
    name='test_login'
),

path(
    'test-verify-otp/',
    views.test_verify_otp,
    name='test_verify_otp'
),

path(
    'test-patient-cards/',
    views.test_patient_cards,
    name='test_patient_cards'
),

path(
    'test-add-patient/',
    views.test_add_patient,
    name='test_add_patient'
),









]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.views.generic import TemplateView

urlpatterns += [
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
