from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
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
from firebase_admin import auth, credentials
import json



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
    """
    API endpoint pour gérer les administrateurs.
    Requiert une authentification Firebase.
    
    create:
    Créer un nouvel administrateur.
    Header requis: Authorization: Bearer <firebase_token>
    
    list:
    Lister tous les administrateurs.
    Header requis: Authorization: Bearer <firebase_token>
    """
    permission_classes = [AllowAny]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def verify_firebase_token(self, token):
        try:
            print("\n=== Début de la vérification du token ===")
            print(f"Token reçu (premiers caractères): {token[:50]}...")
            
            # Vérification directe avec firebase-admin
            decoded_token = auth.verify_id_token(token, check_revoked=True)
            
            print("=== Token décodé avec succès ===")
            print(json.dumps(decoded_token, indent=2))
            return decoded_token
            
        except auth.RevokedIdTokenError:
            print("Erreur: Token révoqué")
            return None
        except auth.InvalidIdTokenError:
            print("Erreur: Token invalide")
            return None
        except auth.ExpiredIdTokenError:
            print("Erreur: Token expiré")
            return None
        except Exception as e:
            print(f"Erreur inattendue: {str(e)}")
            return None

    def create(self, request, *args, **kwargs):
        try:
            print("\n=== Début de la requête POST /api/admins/ ===")
            print("Headers reçus:", dict(request.headers))
            
            auth_header = request.headers.get('Authorization', '')
            print(f"Header d'autorisation: {auth_header}")

            if not auth_header:
                print("Erreur: Pas de header d'autorisation")
                return Response(
                    {'error': 'Header d\'autorisation manquant'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not auth_header.startswith('Bearer '):
                print("Erreur: Format du header incorrect")
                return Response(
                    {'error': 'Format du token incorrect. Doit commencer par "Bearer "'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            token = auth_header.replace('Bearer ', '').strip()
            firebase_user = self.verify_firebase_token(token)

            if not firebase_user:
                print("Erreur: Échec de la vérification du token")
                return Response(
                    {'error': 'Token invalide ou expiré'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            print("=== Utilisateur Firebase authentifié ===")
            print(f"Email: {firebase_user.get('email')}")
            print(f"UID: {firebase_user.get('uid')}")

            return super().create(request, *args, **kwargs)

        except Exception as e:
            print(f"Erreur inattendue dans create: {str(e)}")
            return Response(
                {'error': f'Erreur serveur: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        # Même logique pour la liste
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'No token provided'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split('Bearer ')[1]
        firebase_user = self.verify_firebase_token(token)
        
        if not firebase_user:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().list(request, *args, **kwargs)


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
