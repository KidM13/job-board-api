from rest_framework import serializers
from .models import Company , Job,Application

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields=['id','name','description','website','recruiter']
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields=['id','title','company','description','location','salary_min','salary_max','job_type','is_active','deadline']

