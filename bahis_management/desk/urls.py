from django.urls import path

from bahis_management.desk import views

app_name = "desk"
urlpatterns = [
    path("", views.ModuleList.as_view(), name="list"),
    path("create/", views.ModuleCreate.as_view(), name="create"),
    path("update/<int:pk>/", views.ModuleUpdate.as_view(), name="update"),
    path("delete/<int:pk>/", views.ModuleDelete.as_view(), name="delete"),
    path("workflows/<str:source_form>/", views.WorkflowList.as_view(), name="workflows_list"),
    path("workflows/create/", views.WorkflowCreate.as_view(), name="workflows_create"),
    path("workflows/update/<int:pk>/", views.WorkflowUpdate.as_view(), name="workflows_update"),
    path("workflows/delete/<int:pk>/", views.WorkflowDelete.as_view(), name="workflows_delete"),
]
