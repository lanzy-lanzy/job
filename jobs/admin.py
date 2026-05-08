from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .models import JobPost, Application, ApplicantProfile, SavedJob


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'job_type', 'location', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'job_type', 'created_at']
    search_fields = ['title', 'company_name', 'location']
    ordering = ['-created_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'job', 'user', 'status', 'applied_date']
    list_filter = ['status', 'applied_date']
    search_fields = ['full_name', 'email', 'job__title']
    ordering = ['-applied_date']
    raw_id_fields = ['user']
    list_editable = ['status']
    actions = ['make_accepted', 'make_rejected', 'make_reviewed', 'make_interview', 'make_pending']

    @admin.action(description='Mark selected applications as Accepted')
    def make_accepted(self, request, queryset):
        queryset.update(status='Accepted')

    @admin.action(description='Mark selected applications as Rejected')
    def make_rejected(self, request, queryset):
        queryset.update(status='Rejected')

    @admin.action(description='Mark selected applications as Reviewed')
    def make_reviewed(self, request, queryset):
        queryset.update(status='Reviewed')

    @admin.action(description='Mark selected applications as Interview')
    def make_interview(self, request, queryset):
        queryset.update(status='Interview')

    @admin.action(description='Mark selected applications as Pending')
    def make_pending(self, request, queryset):
        queryset.update(status='Pending')


@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    list_select_related = ['user']


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'job__title']
    raw_id_fields = ['user', 'job']
