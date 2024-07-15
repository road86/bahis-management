from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from bahis_management.desk.api.views import ModuleTypeViewSet, ModuleViewSet, WorkflowViewSet
from bahis_management.taxonomies.api.views import (
    AdministrativeRegionCatchmentView,
    AdministrativeRegionLevelViewSet,
    AdministrativeRegionViewSet,
    TaxonomyViewSet,
)
from users.views import APIAuth

# API Routers
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("desk/modules", ModuleViewSet, basename="Module")
router.register("desk/module-types", ModuleTypeViewSet)
router.register("desk/workflows", WorkflowViewSet)
router.register("taxonomy/administrative-regions", AdministrativeRegionViewSet)
router.register("taxonomy/administrative-region-levels", AdministrativeRegionLevelViewSet)
router.register("taxonomy/taxonomies", TaxonomyViewSet)

app_name = "api"
urlpatterns = router.urls

# Custom API Endpoints
urlpatterns.append(
    path(
        "taxonomy/administrative-regions-catchment/",
        AdministrativeRegionCatchmentView.as_view(),
    )
)
# api login endpoints
urlpatterns.append(path("auth/", APIAuth.as_view()))
