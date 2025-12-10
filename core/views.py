from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Company
from .serializers import UserSerializer, CompanySerializer
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Endpoint para obtener datos del usuario logueado"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login_view(request):
    """
    Login Híbrido:
    1. Autentica al usuario.
    2. Inicia sesión de Django (Session Cookie) para que funcionen las Vistas protegidas.
    3. Devuelve los Tokens JWT para que funcione la API desde el Frontend.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Validamos credenciales
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # PASO CLAVE: Crear la sesión de Django (la cookie)
        login(request, user)
        
        # Generar tokens manualmente
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
        })
    else:
        return Response({'detail': 'Credenciales inválidas'}, status=401)