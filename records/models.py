from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Patient(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)

class DoctorPatientMapping(models.Model):
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE,related_name='patient_mapping')
    doctor = models.ForeignKey('Doctor',on_delete=models.CASCADE,related_name='doctor_mapping')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('patient','doctor')



