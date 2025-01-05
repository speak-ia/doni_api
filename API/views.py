from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Organisation, Admin, Enquete, Enqueteur, EnqueteAssignment
from .serializers import (
    OrganisationSerializer,
    AdminSerializer,
    EnqueteSerializer,
    EnqueteurSerializer,
    EnqueteAssignmentSerializer,
)
from .permissions import IsAdmin, IsPublishedOrAdmin, IsEnqueteur
from django.conf import settings



def firebase_auth_middleware(request):
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        return None

    try:
        user = settings.firebase.auth().verify_id_token(auth_token.split("Bearer ")[-1])
        return user
    except Exception as e:
        print(f"Firebase Auth Error: {e}")
        return None



class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated, IsAdmin]



    def create(self, request, *args, **kwargs):
        # Example of Firebase Authentication Integration
        firebase_user = firebase_auth_middleware(request)
        if firebase_user is None:
            return Response({'error': 'Unauthorized'}, status=401)
        return super().create(request, *args, **kwargs)


class EnqueteViewSet(viewsets.ModelViewSet):
    queryset = Enquete.objects.all()
    serializer_class = EnqueteSerializer
    permission_classes = [IsAuthenticated, IsPublishedOrAdmin]

    def perform_create(self, serializer):
        firebase_user = firebase_auth_middleware(self.request)
        if firebase_user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer.save(created_by=self.request.user.admin)

    def perform_update(self, serializer):
        # Seuls les admins peuvent mettre à jour une enquête
        if not hasattr(self.request.user, 'admin'):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()


class EnqueteurViewSet(viewsets.ModelViewSet):
    queryset = Enqueteur.objects.all()
    serializer_class = EnqueteurSerializer
    permission_classes = [IsAuthenticated, IsEnqueteur]

    def list(self, request, *args, **kwargs):
        # Les enquêteurs voient uniquement leurs propres informations
        if hasattr(request.user, 'enqueteur'):
            self.queryset = self.queryset.filter(id=request.user.enqueteur.id)
        return super().list(request, *args, **kwargs)

class EnqueteAssignmentViewSet(viewsets.ModelViewSet):
    queryset = EnqueteAssignment.objects.all()
    serializer_class = EnqueteAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Les admins voient toutes les candidatures
        if hasattr(self.request.user, 'admin'):
            return self.queryset
        # Les enquêteurs voient uniquement leurs propres candidatures
        elif hasattr(self.request.user, 'enqueteur'):
            return self.queryset.filter(enqueteur=self.request.user.enqueteur)
        return self.queryset.none()

    def perform_update(self, serializer):
        # Seuls les admins peuvent mettre à jour les candidatures
        if not hasattr(self.request.user, 'admin'):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
