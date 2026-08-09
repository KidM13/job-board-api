from rest_framework import serializers
from .models import Company , Job,Application

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields=['id','name','description','website','recruiter']
        read_only_fields=['recruiter']
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields=['id','title','company','description','location','salary_min','salary_max','job_type','is_active','deadline']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        fields=['id','job','user','applied_at','status']
        read_only_fields=['user','status','applied_at']
    def validate(self, data):
        user = self.context['request'].user
        job = data['job']
        if Application.objects.filter(user=user, job=job).exists():
            raise serializers.ValidationError("You have already applied to this job.")

        return data