from django.urls import path

from bahis_management.taxonomies import views

app_name = "taxonomies"
urlpatterns = [
    path("", views.index, name="index"),
    path("taxonomies/list/", views.TaxonomyList.as_view(), name="list"),
    path("taxonomies/create/", views.TaxonomyCreate.as_view(), name="create"),
    path("taxonomies/update/<int:pk>/", views.TaxonomyUpdate.as_view(), name="update"),
    path("taxonomies/delete/<int:pk>/", views.TaxonomyDelete.as_view(), name="delete"),
    path("adminstrative-regions/", views.AdministrativeRegionList.as_view(), name="adminstrative_region_list"),
    path(
        "adminstrative-regions/create/", views.AdministrativeRegionCreate.as_view(), name="adminstrative_region_create"
    ),
    path(
        "adminstrative-regions/update/<int:pk>/",
        views.AdministrativeRegionUpdate.as_view(),
        name="adminstrative_region_update",
    ),
    path(
        "adminstrative-regions/delete/<int:pk>/",
        views.AdministrativeRegionDelete.as_view(),
        name="adminstrative_region_delete",
    ),
    path(
        "adminstrative-region-levels/",
        views.AdministrativeRegionLevelList.as_view(),
        name="adminstrative_region_level_list",
    ),
    path(
        "adminstrative-region-levels/create/",
        views.AdministrativeRegionLevelCreate.as_view(),
        name="adminstrative_region_level_create",
    ),
    path(
        "adminstrative-region-levels/update/<int:pk>/",
        views.AdministrativeRegionLevelUpdate.as_view(),
        name="adminstrative_region_level_update",
    ),
    path(
        "adminstrative-region-levels/delete/<int:pk>/",
        views.AdministrativeRegionLevelDelete.as_view(),
        name="adminstrative_region_level_delete",
    ),
]
