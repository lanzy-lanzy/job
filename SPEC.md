# Job Posting and Application System - Specification

## Project Overview
- **Name**: JobHub
- **Type**: Django web application
- **Core Functionality**: Employers post jobs; applicants apply online with resume upload
- **Stack**: Django + Tailwind CSS (CDN) + Alpine.js (CDN) + HTMX (CDN)

---

## 1. Authentication Module

### Admin Login/Logout
- Single login page at `/login/`
- Django session-based authentication
- Admin-only access for job management and applicant review
- Logout clears session, redirects to login

---

## 2. Job Posting Module (Admin)

### Features
- List all job posts at `/admin/jobs/`
- Create job at `/admin/jobs/create/`
- Edit job at `/admin/jobs/<id>/edit/`
- Delete job with confirmation modal
- View applications for each job at `/admin/jobs/<id>/applications/`

### Job Post Fields
| Field | Type | Validation |
|-------|------|------------|
| title | CharField(255) | required |
| company_name | CharField(255) | required |
| job_type | CharField(100) | choices: Full-time, Part-time, Contract, Internship |
| location | CharField(255) | required |
| salary_range | CharField(100) | optional |
| description | TextField | required |
| qualifications | TextField | required |
| requirements | TextField | required |
| deadline | DateField | required, must be future date |
| status | CharField(20) | choices: Open, Closed; default: Open |
| created_at | DateTimeField | auto |

---

## 3. Job Listing Module (Public)

### Features
- Home page at `/` shows all open jobs in card grid
- Live search via HTMX (no page reload)
- Filter by job_type and location
- Responsive 1-3 column card layout

### Job Card Display
- Title, company, location, job type
- Salary range (if available)
- Posted date and deadline
- "View Details" button

---

## 4. Job Detail Module (Public)

### Features
- Full job details at `/jobs/<id>/`
- Includes: description, qualifications, requirements
- "Apply Now" button opens HTMX modal with application form
- Shows application deadline
- Shows status (Open/Closed)

---

## 5. Application Module (Applicant)

### Features
- Modal form triggered from job detail page
- Fields via HTMX form submission

### Application Fields
| Field | Type | Validation |
|-------|------|------------|
| full_name | CharField(255) | required |
| email | EmailField | required |
| phone | CharField(20) | required |
| address | CharField(500) | required |
| cover_letter | TextField | required |
| resume | FileField | required, PDF/DOC/DOCX, max 5MB |
| applied_date | DateTimeField | auto_now_add |
| status | CharField(20) | default: Pending |
| job | ForeignKey | links to JobPost |

---

## 6. Application Management Module (Admin)

### Features
- View applications per job at `/admin/jobs/<id>/applications/`
- List shows: applicant name, email, applied date, status, resume download
- HTMX inline status update (no page reload)
- Filter by status: All, Pending, Reviewed, Interview, Accepted, Rejected
- Resume download link

---

## 7. Visual Design

### Color Palette
Four color themes available (Blue default, Green, Purple, Orange) with light and dark modes:

#### Blue Theme (Default)
| Element | Light Mode | Dark Mode |
|---------|------------|-----------|
| Primary | `#2563eb` | `#2563eb` |
| Background | `#f8fafc` | `#0f172a` |
| Card BG | `#ffffff` | `#1e293b` |
| Text Primary | `#0f172a` | `#f1f5f9` |
| Text Secondary | `#64748b` | `#94a3b8` |

### Typography
- Font: Inter (system-ui fallback)
- Headings: font-semibold, slate-900 / slate-100 (dark)
- Body: font-normal, slate-700 / slate-300 (dark)

### Components
- Cards: white/slate-800 bg, rounded-xl, shadow-sm, border
- Buttons: rounded-lg, px-4 py-2, transition
- Form inputs: rounded-md, border, focus ring
- Modals: centered, backdrop blur

### Theme Switcher
- Floating button in bottom-right corner (palette icon)
- Toggle drawer with dark mode switch + 4 color themes
- Themes: Blue, Green, Purple, Orange
- Persisted to localStorage
- System dark mode preference detected on first load

### 11. Theme and Dark Mode

| Feature | Implementation |
|---------|----------------|
| Dark Mode Toggle | Switch in theme drawer, persisted in localStorage |
| Color Themes | Blue, Green, Purple, Orange selectable via drawer |
| CSS Variables | `--theme-primary-*`, `--theme-bg`, `--theme-card-bg`, etc. |
| Tailwind Integration | `primary-*` colors update dynamically with theme |
| Persistence | localStorage: `jobhub-theme`, `jobhub-dark` |
| System Preference | `prefers-color-scheme` media query on first visit |

---

## 12. Page Structure

### Public Pages
- `/` - Job listing with search/filter
- `/jobs/<id>/` - Job detail
- `/apply/<job_id>/` - HTMX modal form

### Admin Pages
- `/admin/` - Admin dashboard
- `/admin/jobs/` - Job list
- `/admin/jobs/create/` - Create job
- `/admin/jobs/<id>/edit/` - Edit job
- `/admin/jobs/<id>/delete/` - Delete job
- `/admin/jobs/<id>/applications/` - View applications

### Auth Pages
- `/login/` - Login form
- `/logout/` - Logout action

---

## 13. HTMX Interactions

| Element | Trigger | Action |
|---------|---------|--------|
| Search input | `hx-trigger="input changed, 300ms delay"` | `GET /` with search params |
| Filter select | `change` | `GET /` with filter params |
| Apply button | `click` | Load modal with form |
| Form submit | `submit` | `POST /apply/<job_id>/`, show success |
| Status dropdown | `change` | `POST /admin/applications/<id>/status/` |
| Delete button | `click` | Confirm modal, then `DELETE` |

---

## 14. Acceptance Criteria

- [x] Admin can login and logout
- [x] Admin can create, edit, delete job posts
- [x] Job posts display correctly on home page
- [x] Search filters jobs by title/company without page reload
- [x] Job detail page shows full information
- [x] Applicant can submit application via modal
- [x] Resume file uploads work (PDF, DOC, DOCX under 5MB)
- [x] Admin can view all applications per job
- [x] Admin can update application status via HTMX
- [x] All forms validate properly
- [x] Responsive design works on mobile
- [x] No console errors
- [x] Theme switcher floating button visible on all pages
- [x] Dark mode toggle works and persists across sessions
- [x] Four color themes (Blue, Green, Purple, Orange) selectable
- [x] Theme preference persists in localStorage
- [x] System dark mode preference detected on first visit