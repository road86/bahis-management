from bahis_management.desk.api.views import (
    ModuleTypeViewSet,
    ModuleViewSet,
    WorkflowViewSet,
)
from bahis_management.taxonomies.api.views import (
    AdministrativeRegionCatchmentView,
    AdministrativeRegionLevelViewSet,
    AdministrativeRegionViewSet,
    TaxonomyViewSet,
)
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter


# API Routers
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("desk/modules", ModuleViewSet)
router.register("desk/module-types", ModuleTypeViewSet)
router.register("desk/workflows", WorkflowViewSet)
router.register("taxonomy/administrative-regions", AdministrativeRegionViewSet)
router.register(
    "taxonomy/administrative-region-levels", AdministrativeRegionLevelViewSet
)
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
