from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .models import JobPost, Application, ApplicantProfile, SavedJob
from .forms import JobPostForm, ApplicationForm, ApplicantRegistrationForm, ApplicantLoginForm, ApplicantProfileForm


from functools import wraps

def is_admin(user):
    return user.is_authenticated and user.is_staff


def is_applicant(user):
    return user.is_authenticated and not user.is_staff


def applicant_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path(), login_url='/applicant/login/')
        if request.user.is_staff:
            from django.shortcuts import redirect
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# Public Views
def home(request):
    search = request.GET.get('search', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')

    jobs = JobPost.objects.filter(status='Open')

    if search:
        jobs = jobs.filter(title__icontains=search) | jobs.filter(company_name__icontains=search)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)

    jobs = jobs.distinct()

    # Get unique locations for filter
    locations = JobPost.objects.filter(status='Open').values_list('location', flat=True).distinct()

    # Get saved job IDs for logged-in applicants
    saved_job_ids = []
    if request.user.is_authenticated and not request.user.is_staff:
        saved_job_ids = list(SavedJob.objects.filter(
            job__in=jobs.values_list('id', flat=True)
        ).values_list('job_id', flat=True))

    context = {
        'jobs': jobs,
        'search': search,
        'job_type': job_type,
        'location_filter': location,
        'job_types': JobPost.JOB_TYPE_CHOICES,
        'locations': [l for l in locations if l],
        'is_empty': not jobs.exists(),
        'saved_job_ids': saved_job_ids,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'jobs/partials/job_list.html', context)

    return render(request, 'jobs/home.html', context)


def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    is_saved = False
    if request.user.is_authenticated and not request.user.is_staff:
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
    context = {'job': job, 'is_saved': is_saved}
    return render(request, 'jobs/job_detail.html', context)


@require_http_methods(["GET", "POST"])
def apply_modal(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)

    if job.status != 'Open':
        return HttpResponse('<div class="p-6 text-center text-slate-500">This position is no longer accepting applications.</div>')

    # Pre-populate form for authenticated applicants
    initial_data = {}
    if request.user.is_authenticated and not request.user.is_staff:
        try:
            profile = request.user.applicant_profile
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
                'phone': profile.phone,
                'address': profile.address,
            }
        except ApplicantProfile.DoesNotExist:
            initial_data = {'email': request.user.email}

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            if request.user.is_authenticated and not request.user.is_staff:
                application.user = request.user
            application.save()
            return render(request, 'jobs/partials/application_success.html')
        context = {'form': form, 'job': job, 'errors': form.errors}
    else:
        context = {'form': ApplicationForm(initial=initial_data), 'job': job}

    return render(request, 'jobs/partials/application_form.html', context)


# Admin Views
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        return render(request, 'jobs/admin/login.html', {'error': 'Invalid credentials or access denied.'})

    return render(request, 'jobs/admin/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_jobs = JobPost.objects.count()
    open_jobs = JobPost.objects.filter(status='Open').count()
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status='Pending').count()

    recent_applications = Application.objects.select_related('job').order_by('-applied_date')[:5]

    context = {
        'total_jobs': total_jobs,
        'open_jobs': open_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'recent_applications': recent_applications,
    }
    return render(request, 'jobs/admin/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_job_list(request):
    jobs = JobPost.objects.all().prefetch_related('applications')
    return render(request, 'jobs/admin/job_list.html', {'jobs': jobs})


@login_required
@user_passes_test(is_admin)
def admin_job_create(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_job_list')
    else:
        form = JobPostForm()

    return render(request, 'jobs/admin/job_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(is_admin)
def admin_job_edit(request, pk):
    job = get_object_or_404(JobPost, pk=pk)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('admin_job_list')
    else:
        form = JobPostForm(instance=job)

    return render(request, 'jobs/admin/job_form.html', {'form': form, 'job': job, 'action': 'Edit'})


@login_required
@user_passes_test(is_admin)
def admin_job_delete(request, pk):
    job = get_object_or_404(JobPost, pk=pk)

    if request.method == 'POST':
        job.delete()
        return redirect('admin_job_list')

    return render(request, 'jobs/admin/job_confirm_delete.html', {'job': job})


@login_required
@user_passes_test(is_admin)
def admin_job_applications(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)
    status_filter = request.GET.get('status', '')

    applications = job.applications.select_related()
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'job': job,
        'applications': applications,
        'status_filter': status_filter,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'jobs/admin/job_applications.html', context)


@require_http_methods(["POST"])
@login_required
@user_passes_test(is_admin)
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)
    new_status = request.POST.get('status')

    if new_status in dict(Application.STATUS_CHOICES):
        application.status = new_status
        application.save()

        if request.headers.get('HX-Request'):
            return render(request, 'jobs/admin/partials/application_row.html', {
                'application': application,
                'status_choices': Application.STATUS_CHOICES
            })

        return JsonResponse({'success': True, 'status': new_status})

    return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)


@login_required
@user_passes_test(is_admin)
def admin_applicant_list(request):
    """Admin view to list all applicants across all jobs."""
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')

    applications = Application.objects.select_related('job').order_by('-applied_date')

    if status_filter:
        applications = applications.filter(status=status_filter)

    if search_query:
        applications = applications.filter(
            full_name__icontains=search_query
        ) | applications.filter(
            email__icontains=search_query
        ) | applications.filter(
            job__title__icontains=search_query
        )

    # Pagination
    paginator = Paginator(applications, 20)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    context = {
        'applications': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Application.STATUS_CHOICES,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'jobs/admin/applicant_list.html', context)


@login_required
@user_passes_test(is_admin)
def admin_applicant_detail(request, pk):
    """Admin view to see full details of a single application."""
    application = get_object_or_404(Application.objects.select_related('job'), pk=pk)
    context = {
        'application': application,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'jobs/admin/applicant_detail.html', context)

# Applicant Authentication Views
@require_http_methods(["GET", "POST"])
def applicant_register(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('applicant_dashboard')
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)

    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Complete your profile.')
            return redirect('applicant_profile')
        context = {'form': form}
    else:
        form = ApplicantRegistrationForm()
        context = {'form': form}

    return render(request, 'jobs/applicant/register.html', context)


@require_http_methods(["GET", "POST"])
def applicant_login(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('applicant_dashboard')
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = ApplicantLoginForm(request.POST)
        username = form.data.get('username')
        password = form.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user and not user.is_staff:
            login(request, user)
            next_url = request.GET.get('next', 'applicant_dashboard')
            return redirect(next_url)
        elif user and user.is_staff:
            context = {'form': form, 'error': 'Use admin login for staff access.'}
            return render(request, 'jobs/applicant/login.html', context)
        context = {'form': form, 'error': 'Invalid credentials. Please try again.'}
    else:
        form = ApplicantLoginForm()
        context = {'form': form}

    return render(request, 'jobs/applicant/login.html', context)


def applicant_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# Applicant Dashboard
@applicant_required
def applicant_dashboard(request):
    applications = Application.objects.filter(
        user=request.user
    ).select_related('job').order_by('-applied_date')

    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).select_related('job')

    context = {
        'applications': applications,
        'saved_jobs': saved_jobs,
        'status_counts': {
            'total': applications.count(),
            'pending': applications.filter(status='Pending').count(),
            'reviewed': applications.filter(status='Reviewed').count(),
            'interview': applications.filter(status='Interview').count(),
            'accepted': applications.filter(status='Accepted').count(),
            'rejected': applications.filter(status='Rejected').count(),
        }
    }
    return render(request, 'jobs/applicant/dashboard.html', context)


@require_http_methods(["GET", "POST"])
@applicant_required
def applicant_profile(request):
    profile, _ = ApplicantProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('applicant_profile')
    else:
        form = ApplicantProfileForm(instance=profile)

    return render(request, 'jobs/applicant/profile.html', {
        'form': form,
        'profile': profile
    })


# Saved Jobs
@applicant_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/applicant/saved_jobs.html', {'saved_jobs': saved})


@require_http_methods(["POST"])
@applicant_required
def save_job(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)
    SavedJob.objects.get_or_create(user=request.user, job=job)

    if request.headers.get('HX-Request'):
        return render(request, 'jobs/partials/save_button.html', {
            'job': job,
            'is_saved': True
        })

    return JsonResponse({'saved': True})


@require_http_methods(["POST"])
@applicant_required
def unsave_job(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)
    deleted, _ = SavedJob.objects.filter(user=request.user, job=job).delete()

    if request.headers.get('HX-Request'):
        return render(request, 'jobs/partials/save_button.html', {
            'job': job,
            'is_saved': False
        })

    return JsonResponse({'deleted': deleted > 0})
