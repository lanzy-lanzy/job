from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('apply/<int:job_id>/', views.apply_modal, name='apply_modal'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Applicant Auth
    path('applicant/register/', views.applicant_register, name='applicant_register'),
    path('applicant/login/', views.applicant_login, name='applicant_login'),
    path('applicant/logout/', views.applicant_logout, name='applicant_logout'),

    # Applicant Dashboard
    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('applicant/profile/', views.applicant_profile, name='applicant_profile'),
    path('applicant/saved/', views.saved_jobs, name='saved_jobs'),

    # Saved Jobs HTMX
    path('applicant/save-job/<int:job_id>/', views.save_job, name='save_job'),
    path('applicant/unsave-job/<int:job_id>/', views.unsave_job, name='unsave_job'),

    # Admin views
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/jobs/', views.admin_job_list, name='admin_job_list'),
    path('admin/jobs/create/', views.admin_job_create, name='admin_job_create'),
    path('admin/jobs/<int:pk>/edit/', views.admin_job_edit, name='admin_job_edit'),
    path('admin/jobs/<int:pk>/delete/', views.admin_job_delete, name='admin_job_delete'),
    path('admin/jobs/<int:job_id>/applications/', views.admin_job_applications, name='admin_job_applications'),
    path('admin/applicants/', views.admin_applicant_list, name='admin_applicant_list'),
    path('admin/applicants/<int:pk>/', views.admin_applicant_detail, name='admin_applicant_detail'),

    # HTMX API
    path('admin/applications/<int:pk>/status/', views.update_application_status, name='update_application_status'),
]