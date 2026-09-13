
from django.contrib.auth.models import User
from .models import Patient, Doctor, DoctorPatientMapping
from django.contrib.auth.password_validation import validate_password
from rest_framework import status, serializers
from rest_framework.validators import UniqueTogetherValidator
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(write_only  = True,required = True)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['name','email','created_by']
        extra_kwargs = {
            'created_by':{'read_only':True}
        }
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name','email','created_by']
        extra_kwargs = {
            'created_by':{'read_only':True}
        }

class PatientDoctorSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset = Doctor.objects.all())
    patient = serializers.PrimaryKeyRelatedField(queryset = Patient.objects.all())
    class Meta:
        model = DoctorPatientMapping
        fields = ['id','doctor','patient']
        validators = [UniqueTogetherValidator(queryset= DoctorPatientMapping.objects.all(), fields = ['doctor','patient'], message="This doctor is already assigned to this patient")]

    def validate_patient(self, patient):
        request = self.context.get('request')
        if patient.created_by != request.user:
            raise serializers.ValidationError('you are not authorized to use current patient')
        return patient