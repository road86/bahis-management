from django.db import models


class ModuleType(models.Model):
    """
    This model is used to define the type of module that is being created.
    Each module type will be linked to a definition inside the BAHIS-desk app.
    This is used to create logical branches for data processing
    (pulling / pushing) and also for frontend rendering of the modules.
    """

    title = models.CharField(
        max_length=150,
        help_text="The type of module as understood by the BAHIS-desk app",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    """
    This model is used to define the modules that will be rendered in the BAHIS-desk app.
    """

    title = models.CharField(
        max_length=150,
        help_text="The title of the module, this will be rendered in the BAHIS-desk app",
    )
    icon = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="The icon to be used from the MUI icons set (https://mui.com/material-ui/material-icons)",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="A description of the module, this will be rendered in the BAHIS-desk app",
    )
    form = models.TextField(
        blank=True,
        null=True,
        help_text="The form to be used for this module (if type is form or list)",
    )  # TODO how to import from kobo in bahis 3, as a URL?, also - how to handle offline forms?
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="The external URL to be used for this module (if type is external URL)",
    )
    module_type = models.ForeignKey(
        ModuleType,
        on_delete=models.CASCADE,
        help_text="The module type as understood by the BAHIS-desk app",
    )
    parent_module = models.ForeignKey(
        "Module",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The parent module for this module if part of a heiarchy",
    )
    sort_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="The sort order for this module in the BAHIS-desk app (smaller means higher)",
    )
    is_active = models.BooleanField(default=True, help_text="Whether this module is active in the BAHIS-desk app")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Workflow(models.Model):
    """
    This model is used to define the workflows for a module,
    such as follow up and closure forms, which will be rendered in the BAHIS-desk app.
    """

    title = models.CharField(
        max_length=150,
        help_text="The title of the workflow, this will be rendered as a button in the BAHIS-desk app",
    )
    source_form = models.TextField(
        blank=True, null=True, help_text="The source form for this workflow"
    )  # TODO how to import from kobo in bahis 3, as a URL?, also - how to handle offline forms?
    destination_form = models.TextField(
        blank=True, null=True, help_text="The destination form for this workflow"
    )  # TODO how to import from kobo in bahis 3, as a URL?, also - how to handle offline forms?
    definition = models.JSONField(
        help_text="A JSON object mapping fields from the source form to fields in the destination form"
    )
    is_active = models.BooleanField(default=True, help_text="Whether this workflow is active in the BAHIS-desk app")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
