from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import StudentRecord
from .permissions import IsAdminUser, IsAdminOrFaculty, IsAdminFacultyOrOwner
from .serializers import StudentRecordSerializer, UserRegistrationSerializer

class StudentRecordViewSet(ModelViewSet):
    serializer_class = StudentRecordSerializer

    def get_queryset(self):
        user = self.request.user
        # Admins and Faculty see all records
        if user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return StudentRecord.objects.all().select_related('owner')
        # Students see only their own record
        return StudentRecord.objects.filter(owner=user).select_related('owner')

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = [IsAdminUser]
        elif self.action in ('update', 'partial_update'):
            permission_classes = [IsAdminOrFaculty]
        elif self.action == 'retrieve':
            permission_classes = [IsAdminFacultyOrOwner]
        else:  # list
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        owner_id = self.request.data.get('owner')
        try:
            owner = User.objects.get(pk=owner_id) if owner_id else self.request.user
        except User.DoesNotExist:
            owner = self.request.user
        serializer.save(owner=owner)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.full_name
        self.perform_destroy(instance)
        return Response({'detail': f"Record for '{name}' deleted."},
                        status=status.HTTP_200_OK)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)