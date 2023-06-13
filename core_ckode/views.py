from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User, Lead, Project
from .serializers import UserSerializer, LeadSerializer, ProjectSerializer
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.db import connection


class AuthenticateView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            user.last_login = timezone.now()  # Atualiza o campo last_login em UTC
            user.save()

        response = super().post(request, *args, **kwargs)

        refresh_token = response.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)

            token.set_exp(lifetime=timedelta(days=30))  # Tempo de expiração do refresh token
            refresh_token = str(token)  # Obtém o novo refresh token com o tempo de expiração definido
            response.data['refresh'] = refresh_token  # Atualiza o valor do refresh token na resposta

            access_token = response.data.get('access')
            response.set_cookie(key='jwt', value=access_token, httponly=True)

        if user is not None:
            response.data['user'] = user.name

        return response


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = User.objects.get(id=user_id)
        data = request.data.copy()
        password = data.pop('password', None)
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        if password is not None:
            user.set_password(password)
            user.save()
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'response': 'success'}, status=status.HTTP_200_OK)


class LeadView(APIView):
    permission_classes = [IsAuthenticated]  # Aqui estou configurando a view para exigir um token de autenticação para ser acessada.

    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        leads = Lead.objects.all()
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)

    def put(self, request, lead_id):
        body = request.data
        lead = Lead.objects.get(id=lead_id)

        lead_s = LeadSerializer(lead, data=body)
        lead_s.is_valid(raise_exception=True)
        lead_s.save()
        return Response(data=lead_s.data)

    def delete(self, request, lead_id):
        lead = Lead.objects.get(id=lead_id)
        lead.delete()
        return Response({'response': 'success'}, status=status.HTTP_200_OK)


class ProjectView(APIView):
    permission_classes = [IsAuthenticated]  # Aqui estou configurando a view para exigir um token de autenticação para ser acessada.

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def put(self, request, project_id):
        body = request.data
        project = Project.objects.get(id=project_id)

        project_s = ProjectSerializer(project, data=body)
        project_s.is_valid(raise_exception=True)
        project_s.save()
        return Response(data=project_s.data)

    def delete(self, request, project_id):
        project = Project.objects.get(id=project_id)
        project.delete()
        return Response({'response': 'success'}, status=status.HTTP_200_OK)


class ProjectStatusPercentageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT CASE "
                           "WHEN status = 1 THEN 'In Progress' "
                           "WHEN status = 2 THEN 'Finished' "
                           "WHEN status = 3 THEN 'Closed' "
                           "WHEN status = 4 THEN 'Proposal' "
                           "END AS status_name, ROUND((COUNT(*) * "
                           "100.0) / (SELECT COUNT(*) FROM ckode_projects.projects), 2) AS percentage FROM "
                           "ckode_projects.projects GROUP BY status_name;"
                           "ORDER BY CASE "
                           "WHEN status = 1 THEN 0 "
                           "WHEN status = 4 THEN 1 "
                           "WHEN status = 2 THEN 2 "
                           "WHEN status = 3 THEN 3 "
                           "END;")
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            result = []
            for row in data:
                row_dict = dict(zip(columns, row))
                row_dict['percentage'] = float(row_dict['percentage'])  # Converter para float
                result.append(row_dict)
        return JsonResponse(result, safe=False)


class ProjectStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT CASE "
                           "WHEN status = 1 THEN 'In Progress' "
                           "WHEN status = 2 THEN 'Finished' "
                           "WHEN status = 3 THEN 'Closed' "
                           "WHEN status = 4 THEN 'Proposal' "
                           "END AS status_name, "
                           "COUNT(*) AS quantity FROM ckode_projects.projects "
                           "WHERE status IN (1, 2, 3, 4) GROUP BY status_name "
                           "ORDER BY CASE "
                           "WHEN status = 1 THEN 0 "
                           "WHEN status = 4 THEN 1 "
                           "WHEN status = 2 THEN 2 "
                           "WHEN status = 3 THEN 3 "
                           "END;")
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            result = []
            for row in data:
                row_dict = dict(zip(columns, row))
                row_dict['quantity'] = int(row_dict['quantity'])  # Converter para int
                result.append(row_dict)
        return JsonResponse(result, safe=False)
