from django.shortcuts import render

# Create your views here.
from .models import Company, Job,Application
from rest_framework import viewsets
from .serializers import CompanySerializer, JobSerializer, ApplicationSerializer
from .permission import IsJobCompanyOwner , IsRecruiterOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

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
        company = serializer.validated_data['company']
        if company.recruiter != self.request.user:
            raise PermissionDenied("You can only post jobs under your own company.")
        serializer.save()
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Application.objects.select_related('user', 'job', 'job__company').filter(
            Q(user=user) | Q(job__company__recruiter=user)
        )



