from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from rest_framework import (
    filters,
    generics,
    permissions,
    status,
    viewsets
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Task
from .serializers import (
    CategorySerializer,
    RegisterSerializer,
    TaskSerializer
)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Fornece as ações completas de CRUD (Create, Read, Update, Delete) para as Tarefas.

    - Apenas usuários autenticados podem acessar.
    - As tarefas são automaticamente filtradas por usuário logado.
    - Suporta busca por 'title' e 'description'.
    - Suporta ordenação por 'created_at'.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        Sobrescreve o método padrão para retornar apenas as tarefas
        do usuário atualmente autenticado.
        """
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Sobrescreve o método de criação para associar automaticamente
        a nova tarefa ao usuário atualmente autenticado.
        """
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Fornece as ações completas de CRUD (Create, Read, Update, Delete) para as Categorias.

    - Apenas usuários autenticados podem acessar.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    """
    Endpoint público para registro de novos usuários.
    Não requer autenticação para ser acessado.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


class TaskFilteredListView(APIView):
    """
    Endpoint para listar tarefas com um filtro opcional de data de criação.

    - GET /api/tasks-filtrar/: Retorna todas as tarefas do usuário logado.
    - GET /api/tasks-filtrar/?data_inicial=...&data_final=...:
      Retorna as tarefas do usuário dentro do intervalo de datas especificado.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Lida com requisições GET para listar e filtrar tarefas.

        Parâmetros da URL (opcionais):
        - data_inicial (str): Data de início do filtro (formato ISO 8601).
        - data_final (str): Data de fim do filtro (formato ISO 8601).

        Retorna:
        - Uma lista de tarefas serializadas.
        - Um erro 400 se o formato da data for inválido.
        """
        user = request.user
        params = request.query_params
        tasks = Task.objects.filter(user=user)

        data_inicial_str = params.get('data_inicial')
        data_final_str = params.get('data_final')

        if data_inicial_str and data_final_str:
            try:
                data_inicial = parse_datetime(data_inicial_str)
                data_final = parse_datetime(data_final_str)
                if not data_inicial or not data_final:
                    raise ValueError

                tasks = tasks.filter(
                    created_at__gte=data_inicial,
                    created_at__lte=data_final
                )

            except ValueError:
                return Response(
                    {"error": "Formato de data inválido. Use o formato ISO 8601 (ex: YYYY-MM-DDTHH:MM:SSZ)."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)