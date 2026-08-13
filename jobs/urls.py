from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('api/company-v2',views.CompanyViewset)
router.register('api/job-v2',views.JobViewset)
router.register('api/application-v2',views.ApplicationViewSet,basename='application')

urlpatterns =[
]+router.urls

