# Job Board API

A REST API for a job board platform, built with Django and Django REST Framework. Recruiters create companies and post jobs; job seekers browse, search, and apply — with role-based permissions enforced at every step.

**Live API:** https://job-board-api-vbmk.onrender.com
**Interactive docs (Swagger):** https://job-board-api-vbmk.onrender.com/api/docs/
**Alternative docs (ReDoc):** https://job-board-api-vbmk.onrender.com/api/redoc/

> Note: hosted on Render's free tier — the first request after inactivity may take 30–50 seconds while the instance wakes up.
![Swagger UI overview](screenshots/swagger-overview.png)
>
> ## Features

- **JWT authentication** (access + refresh tokens) via `djangorestframework-simplejwt`
- **Role-based permissions** — only a company's owner can edit/delete it or post jobs under it; only a job's owning recruiter can update an application's status
- **One application per user per job**, enforced at both the database and API level with a clean validation error instead of a server crash
- **Filtering, search, and ordering** on job listings (location, job type, keyword search, sort by deadline/salary)
- **Pagination** and **rate limiting** (separate limits for anonymous vs. authenticated users)
- **Background tasks with Celery + Redis** — notifies a recruiter when someone applies, and a scheduled daily task that automatically deactivates jobs past their deadline
- **Auto-generated API documentation** with `drf-spectacular`
- **Automated test suite** covering the ownership and permission rules, using DRF's `APIClient`
- **CORS** configured for frontend integration

