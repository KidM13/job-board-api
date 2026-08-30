from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Company, Job, Application

class JobPermissionAPITest(TestCase):
    def test_non_owner_cannot_create_job(self):
        userA = User.objects.create_user(username='test', password='test123')
        userB = User.objects.create_user(username='kebede', password='kebede123')
        companyA=Company.objects.create(
            name='userA company',
            description='there is nothing to say about ',
            website='http://companyAwebsite.com',
            recruiter=userA,
        )
        client=APIClient()
        token = RefreshToken.for_user(userB)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
        response = client.post('/api/job-v2/', {
            'title': 'Should Fail',
            'company': companyA.id,
            'description': 'testing',
            'location': 'Remote',
            'salary_min': 1000,
            'salary_max': 2000,
            'job_type': 'remote',
            'deadline': '2026-12-01'
        })
        self.assertEqual(response.status_code,403)

class CompanyPermissionAPITest(TestCase):
    def test_non_owner_cannot_delete_or_edit_company(self):
        userA = User.objects.create_user(username='test', password='test123')
        userB = User.objects.create_user(username='kebede', password='kebede123')
        companyA=Company.objects.create(
                    name='userA company',
                    description='there is nothing to say about ',
                    website='http://companyAwebsite.com',
                    recruiter=userA,
                )
        client=APIClient()
        token = RefreshToken.for_user(userB)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
        response=client.delete(f'/api/company-v2/{companyA.id}/')
        self.assertEqual(response.status_code,403)

class ApplicationPermissionAPITest(TestCase):
    def test_non_owner_cannot_update_job_status(self):
        userA = User.objects.create_user(username='test', password='test123')
        userB = User.objects.create_user(username='kebede', password='kebede123')
        companyA=Company.objects.create(
                            name='userA company',
                            description='there is nothing to say about ',
                            website='http://companyAwebsite.com',
                            recruiter=userA,
                        )
        jobA=Job.objects.create(
            company=companyA,
            title='fullstack developer',
            description='a person who does both the backend and frontend things',
            location= 'Remote',
            salary_min=1000,
            salary_max= 2000,
            job_type= 'remote',
            deadline= '2026-12-01',
            is_active='True'
        )
        applicationB=Application.objects.create(
            user=userB,
            job=jobA
        )
        client=APIClient()
        token = RefreshToken.for_user(userB)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
        response=client.patch(f'/api/application-v2/{applicationB.id}/update_status/',{
          'status':'accepted'
        })
        self.assertEqual(response.status_code,403)
class DuplicateApplicationTest(TestCase):
    def test_prevent_duplicate_application(self):
        userA = User.objects.create_user(username='test', password='test123')
        userB = User.objects.create_user(username='kebede', password='kebede123')
        companyA=Company.objects.create(
                                    name='userA company',
                                    description='there is nothing to say about ',
                                    website='http://companyAwebsite.com',
                                    recruiter=userA,
                                )
        jobA=Job.objects.create(
                    company=companyA,
                    title='fullstack developer',
                    description='a person who does both the backend and frontend things',
                    location= 'Remote',
                    salary_min=1000,
                    salary_max= 2000,
                    job_type= 'remote',
                    deadline= '2026-12-01',
                    is_active='True'
                )
        applicationB=Application.objects.create(
                    user=userB,
                    job=jobA
                )
        client=APIClient()
        token = RefreshToken.for_user(userB)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
        response =client.post('/api/application-v2/',{
            'job':jobA.id
        })
        self.assertEqual(response.status_code,400)#status code 400



