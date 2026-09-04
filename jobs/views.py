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
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .tasks import notify_recruiter

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
    filterset_fields=['location','job_type','is_active']
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields=['title','description']
    ordering_fields=['deadline','salary_min']

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
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        application=self.get_object()
        notify_recruiter.delay(application.id)

    @action(detail=True,methods=['PATCH'])
    def update_status(self,request,pk=None):
        application=self.get_object()
        if application.job.company.recruiter!=self.request.user:
            raise PermissionDenied('only the recruiter who owns this job can update its status')
        new_status=request.data.get('status')
        if new_status not in ['pending','accepted','rejected']:
            return Response({'error':'Invalid status value '},status=400)
        application.status=new_status
        application.save()
        return Response(ApplicationSerializer(application).data)
        
        



