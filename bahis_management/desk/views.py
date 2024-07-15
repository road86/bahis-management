from typing import Any

import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import TextInput
from django.forms.models import BaseModelForm
from django.forms.utils import flatatt
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from rest_framework.authtoken.models import Token

from bahis_management.desk.models import Module, Workflow
from bahis_management.desk.utils import get_modules_for_user
from config.settings.base import env

desk_module_entry_fields = [
    "title",
    "icon",
    "description",
    "form",
    "external_url",
    "module_type",
    "parent_module",
    "sort_order",
    "is_active",
]


def get_kobotoolbox_forms(request):
    # get list of forms from kobotoolbox
    api_url = env("KOBOTOOLBOX_KF_API_URL")
    token = Token.objects.get(user=request.user)
    api_token = token.key
    response = requests.get(f"{api_url}assets/?format=json", headers={"Authorization": f"Token {api_token}"})
    asset_list = response.json().get("results")

    form_options = []
    if asset_list:
        deployed_form_list = [asset for asset in asset_list if asset.get("has_deployment", False)]

        form_options.append({"id": None, "name": "--------", "description": ""})
    else:
        form_options.append(
            {
                "id": None,
                "name": "--------",
                "description": "There are no forms in the BAHIS KoboToolbox instance",
            }
        )

    for form in deployed_form_list:
        form_options.append(
            {
                "id": form.get("uid"),
                "name": form.get("name"),
                "description": form.get("settings", dict()).get("description"),
            }
        )

    return form_options


class KoboToolboxFormPicker(TextInput):
    def __init__(self, request):
        super().__init__()
        self.request = request

    def render(self, name, value, attrs: dict[str, Any] | None = None, **kwargs):
        super().render(name, value, attrs)

        # get list of forms from kobotoolbox
        forms = get_kobotoolbox_forms(self.request)

        form_options = ""
        for form in forms:
            if form["id"] == value:
                form_options += f'<option value="{form["id"]}" selected>{form["name"]}- {form["description"]}</option>'
            else:
                form_options += f'<option value="{form["id"]}">{form["name"]}- {form["description"]}</option>'

        if attrs is not None:
            flat_attrs = flatatt(attrs)
            html = f'  <select name="{name}" {flat_attrs}> ' + form_options + "</select>"
        else:
            html = f'  <select name="{name}"> ' + form_options + "</select>"
        return mark_safe(html)


class MaterialUIIconPicker(TextInput):
    # based on https://codepen.io/mortenson/pen/GMBeEg/
    def render(self, name, value, attrs: dict[str, Any] | None = None, **kwargs):
        super().render(name, value, attrs)

        if attrs is not None:
            flat_attrs = flatatt(attrs)
            if value:
                html = f'<input name={name} {flat_attrs} type="text" class="use-material-icon-picker" value={value}>'
            else:
                html = f'<input name={name} {flat_attrs} type="text" class="use-material-icon-picker">'
        else:
            if value:
                html = f'<input name={name} type="text" class="use-material-icon-picker" value={value}>'
            else:
                html = f'<input name={name} type="text" class="use-material-icon-picker">'
        return mark_safe(html)


class ModuleList(LoginRequiredMixin, FilterView):
    template_name_suffix = "_list"
    model = Module
    paginate_by = 5
    ordering = ["id"]
    filterset_fields = {
        "title": ["icontains"],
        "description": ["icontains"],
        "parent_module": ["exact"],
    }

    def get_queryset(self):
        ids = [i.id for i in get_modules_for_user(self.request)]
        return Module.objects.filter(id__in=ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = dict()
        # remove page from query tag so pagination works in template
        for k, v in context["filter"].data.items():
            if k != "page" and v != "":
                context["query"][k] = v

        # use paginator range with ellipses for simplicity
        page = context["page_obj"]
        context["paginator_range"] = page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=2)

        return context


class ModuleCreate(LoginRequiredMixin, CreateView):
    template_name_suffix = "_create_form"
    model = Module
    fields = desk_module_entry_fields
    success_url = reverse_lazy("desk:list")

    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.fields["icon"].widget = MaterialUIIconPicker()
        form.fields["form"].widget = KoboToolboxFormPicker(self.request)
        return form

    def form_valid(self, form):
        messages.success(self.request, "The module was created successfully.")
        return super(ModuleCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The module was not created successfully.")
        form.error_css_class = "error"
        return super(ModuleCreate, self).form_invalid(form)


class ModuleUpdate(LoginRequiredMixin, UpdateView):
    template_name_suffix = "_update_form"
    model = Module
    fields = desk_module_entry_fields
    success_url = reverse_lazy("desk:list")

    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.fields["icon"].widget = MaterialUIIconPicker()
        form.fields["form"].widget = KoboToolboxFormPicker(self.request)
        return form

    def form_valid(self, form):
        messages.success(self.request, "The module was updated successfully.")
        return super(ModuleUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.module_type.title == "List":
            context["allow_workflows"] = True
        return context


class ModuleDelete(LoginRequiredMixin, DeleteView):
    template_name_suffix = "_delete_form"
    model = Module
    success_url = reverse_lazy("desk:list")

    def form_valid(self, form):
        messages.success(self.request, "The module was deleted successfully.")
        return super(ModuleDelete, self).form_valid(form)


desk_module_workflow_entry_fields = [
    "title",
    "source_form",
    "destination_form",
    "definition",
    "is_active",
]


class WorkflowList(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    model = Workflow
    paginate_by = 5
    ordering = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(source_form__exact=self.kwargs["source_form"])


class WorkflowCreate(LoginRequiredMixin, CreateView):
    template_name_suffix = "_create_form"
    model = Workflow
    fields = desk_module_workflow_entry_fields
    success_url = reverse_lazy("desk:list")

    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.fields["source_form"].widget = KoboToolboxFormPicker(self.request)
        form.fields["destination_form"].widget = KoboToolboxFormPicker(self.request)
        return form

    def form_valid(self, form):
        messages.success(self.request, "The module workflow was created successfully.")
        return super(WorkflowCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The module workflow was not created successfully.")
        form.error_css_class = "error"
        return super(WorkflowCreate, self).form_invalid(form)


class WorkflowUpdate(LoginRequiredMixin, UpdateView):
    template_name_suffix = "_update_form"
    model = Workflow
    fields = desk_module_workflow_entry_fields
    success_url = reverse_lazy("desk:list")

    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.fields["source_form"].widget = KoboToolboxFormPicker(self.request)
        form.fields["destination_form"].widget = KoboToolboxFormPicker(self.request)
        return form

    def form_valid(self, form):
        messages.success(self.request, "The module workflow was updated successfully.")
        return super(WorkflowUpdate, self).form_valid(form)


class WorkflowDelete(LoginRequiredMixin, DeleteView):
    template_name_suffix = "_delete_form"
    model = Workflow
    success_url = reverse_lazy("desk:list")

    def form_valid(self, form):
        messages.success(self.request, "The module workflow was deleted successfully.")
        return super(WorkflowDelete, self).form_valid(form)
