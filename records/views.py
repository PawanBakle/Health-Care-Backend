from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Patient,Doctor,DoctorPatientMapping
from django.contrib.auth.password_validation import validate_password
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import RegisterSerializer, LoginSerializer,PatientSerializer,DoctorSerializer,PatientDoctorSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serialize = RegisterSerializer(data = request.data)
        serialize.is_valid(raise_exception = True)
        serialize.save()
        return Response(serialize.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        serialize = LoginSerializer(data = request.data)
        serialize.is_valid(raise_exception = True)
        username = serialize.validated_data.get('username',None)
        password = serialize.validated_data.get('password',None)

        authenticate_user = authenticate(username = username, password = password)
        if authenticate_user:
            refresh = RefreshToken.for_user(authenticate_user)
            return Response({
                "refresh":str(refresh),
                "access":str(refresh.access_token),

            },status=status.HTTP_200_OK)
        return Response({'detail':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)

class PatientRecords(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        patients = Patient.objects.filter(created_by = request.user)
        serialize = PatientSerializer(patients, many = True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    def post(self, request):
        serialize = PatientSerializer(data = request.data)
        serialize.is_valid(raise_exception=True)
        data = serialize.save(created_by = request.user)
        return Response(serialize.data,status=status.HTTP_201_CREATED)

class PatientsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,pk):
        patient = get_object_or_404(Patient,pk = pk, created_by = request.user)
        serialize = PatientSerializer(patient)
        return Response(serialize.data,status=status.HTTP_200_OK)

    def put(self, request, pk):
        data = get_object_or_404(Patient,pk = pk, created_by = request.user)
        serialize = PatientSerializer(data, data = request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        data = get_object_or_404(Patient,pk = pk, created_by = request.user)
        data.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class DoctorView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)
class DoctorMappingView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PatientDoctorSerializer
    queryset = DoctorPatientMapping.objects.all()

    def retrieve(self, request, pk = None):
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        mapping_orm = DoctorPatientMapping.objects.filter(patient = patient)
        serializer = self.get_serializer(mapping_orm, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    