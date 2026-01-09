from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .models import Match, Over, Batting, Extra
from .serializers import MatchSerializer, OverSerializer, BattingSerializer, ExtraSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserLoginSerializer

User = get_user_model()

# ------------------- Register -------------------
class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------- Login -------------------
class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "message": "Login successful",
                "access": access_token,
                "refresh": refresh_token
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------- Logout -------------------
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist the refresh token
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Requires SimpleJWT blacklist app enabled
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ------------------- Match API -------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def match_list_create(request):
    if request.method == 'GET':
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def match_detail(request, pk):
    try:
        match = Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchSerializer(match)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = MatchSerializer(match, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        match.delete()
        return Response({"message": "Match deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------- Over API (Singleton) -------------------
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def over_api(request):
    over = Over.objects.first()

    if request.method == 'GET':
        if over:
            serializer = OverSerializer(over)
            return Response(serializer.data)
        return Response({"message": "No Over found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = OverSerializer(over, data=request.data) if over else OverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        if not over:
            return Response({"message": "No Over to update"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OverSerializer(over, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not over:
            return Response({"message": "No Over to delete"}, status=status.HTTP_404_NOT_FOUND)
        over.delete()
        return Response({"message": "Over deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------- Batting API -------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def batting_list_create(request):
    if request.method == 'GET':
        batters = Batting.objects.all()
        serializer = BattingSerializer(batters, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BattingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def batting_detail(request, pk):
    try:
        batter = Batting.objects.get(pk=pk)
    except Batting.DoesNotExist:
        return Response({"message": "Batsman not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BattingSerializer(batter)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = BattingSerializer(batter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        batter.delete()
        return Response({"message": "Batsman deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------- Extra API (Singleton) -------------------
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def extra_singleton_api(request):
    extra = Extra.objects.first()

    if request.method == 'GET':
        if extra:
            serializer = ExtraSerializer(extra)
            return Response(serializer.data)
        return Response({"message": "No Extra found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = ExtraSerializer(extra, data=request.data) if extra else ExtraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        if not extra:
            return Response({"message": "No Extra to update"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExtraSerializer(extra, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not extra:
            return Response({"message": "No Extra to delete"}, status=status.HTTP_404_NOT_FOUND)
        extra.delete()
        return Response({"message": "Extra deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------- Dashboard View (Public) -------------------
@api_view(['GET'])
@permission_classes([AllowAny])  # Public access
def dashboard_view(request):
    # Matches
    matches = Match.objects.all()
    match_serializer = MatchSerializer(matches, many=True)

    # Over (singleton)
    over = Over.objects.first()
    over_serializer = OverSerializer(over) if over else None

    # Batting
    batters = Batting.objects.all()
    batting_serializer = BattingSerializer(batters, many=True)

    # Extra (singleton)
    extra = Extra.objects.first()
    extra_serializer = ExtraSerializer(extra) if extra else None

    # Total score calculation
    batting_total = sum(b.runs_scored for b in batters)
    extra_total = sum(e.extra_runs for e in Extra.objects.all()) if extra else 0
    total_score = batting_total + extra_total

    # Combined data
    data = {
        "matches": match_serializer.data,
        "over": over_serializer.data if over_serializer else None,
        "batting": batting_serializer.data,
        "extra": extra_serializer.data if extra_serializer else None,
        "score": {
            "batting_total": batting_total,
            "extra_total": extra_total,
            "total_score": total_score
        }
    }

    return Response(data)
