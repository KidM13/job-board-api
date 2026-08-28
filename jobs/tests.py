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
        