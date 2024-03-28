from rest_framework import permissions, viewsets

from bahis_management.desk.api.serializers import ModuleSerializer, ModuleTypeSerializer, WorkflowSerializer
from bahis_management.desk.models import Module, ModuleType, Workflow


class ModuleTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ModuleTypes to be viewed or edited.
    """

    queryset = ModuleType.objects.all().order_by("id")
    serializer_class = ModuleTypeSerializer
    permission_classes = [permissions.AllowAny]  # [permissions.IsAuthenticated] FIXME auth is turned off


class ModuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Modules to be viewed or edited.
    """

    queryset = Module.objects.all().order_by("parent_module", "sort_order")
    serializer_class = ModuleSerializer
    permission_classes = [permissions.AllowAny]  # [permissions.IsAuthenticated] FIXME auth is turned off


class WorkflowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Workflows to be viewed or edited.
    """

    queryset = Workflow.objects.all().order_by("id")
    serializer_class = WorkflowSerializer
    permission_classes = [permissions.AllowAny]  # [permissions.IsAuthenticated] FIXME auth is turned off
