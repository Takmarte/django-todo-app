from rest_framework import viewsets, permissions
from .models import Todos
from .serializers import TodosSerializer

class TodosViewSet(viewsets.ModelViewSet):
    queryset = Todos.objects.all()
    serializer_class = TodosSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Todos.objects.all()
        return Todos.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)