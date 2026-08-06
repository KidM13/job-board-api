from django.shortcuts import render

# Create your views here.
from .models import Company, Job,Application
from rest_framework import viewsets
from .serializers import CompanySerializer, JobSerializer
from .permission import IsJobCompanyOwner , IsRecruiterOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CompanyViewset(viewsets.ModelViewSet):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    permission_classes=[IsAuthenticatedOrReadOnly,IsRecruiterOwner]
    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)
class JobViewset(viewsets.ModelViewSet):
    queryset=Job.objects.select_related('company')
    serializer_class=JobSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,IsJobCompanyOwner]
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


