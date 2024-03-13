from bahis_management.taxonomies.models import (
    AdministrativeRegion,
    AdministrativeRegionLevel,
    Taxonomy,
)
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView


def index(request):
    context = {}
    context['taxonomies'] = Taxonomy.objects.all()
    return render(request, "taxonomies/index.html", context)


taxonomy_entry_fields = [
    "title",
    "csv_file",
]


class TaxonomyList(ListView):
    template_name_suffix = "_list"
    model = Taxonomy
    paginate_by = 5
    ordering = ["title"]


class TaxonomyCreate(CreateView):
    template_name_suffix = "_create_form"
    model = Taxonomy
    fields = taxonomy_entry_fields
    success_url = reverse_lazy("taxonomies:list")

    def form_valid(self, form):
        print(form)

        messages.success(self.request, "The taxonomy was created successfully.")
        return super(TaxonomyCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The taxonomy was not created successfully.")
        form.error_css_class = "error"
        return super(TaxonomyCreate, self).form_invalid(form)


class TaxonomyUpdate(UpdateView):
    template_name_suffix = "_update_form"
    model = Taxonomy
    fields = taxonomy_entry_fields
    success_url = reverse_lazy("taxonomies:list")

    def form_valid(self, form):
        messages.success(self.request, "The taxonomy was updated successfully.")
        return super(TaxonomyUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The taxonomy was not updated successfully.")
        form.error_css_class = "error"
        return super(TaxonomyUpdate, self).form_invalid(form)


class TaxonomyDelete(DeleteView):
    template_name_suffix = "_delete_form"
    model = Taxonomy
    success_url = reverse_lazy("taxonomies:list")

    def form_valid(self, form):
        messages.success(self.request, "The taxonomy was deleted successfully.")
        return super(TaxonomyDelete, self).form_valid(form)


adminstrative_region_level_entry_fields = [
    "id",
    "title",
]


class AdministrativeRegionLevelList(ListView):
    template_name_suffix = "_list"
    model = AdministrativeRegionLevel
    paginate_by = 5
    ordering = ["id"]


class AdministrativeRegionLevelCreate(CreateView):
    template_name_suffix = "_create_form"
    model = AdministrativeRegionLevel
    fields = adminstrative_region_level_entry_fields
    success_url = reverse_lazy("taxonomies:adminstrative_region_level_list")

    def form_valid(self, form):
        messages.success(self.request, "The administrative region level was created successfully.")
        return super(AdministrativeRegionLevelCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The administrative region level was not created successfully.")
        form.error_css_class = "error"
        return super(AdministrativeRegionLevelCreate, self).form_invalid(form)


class AdministrativeRegionLevelUpdate(UpdateView):
    template_name_suffix = "_update_form"
    model = AdministrativeRegionLevel
    fields = adminstrative_region_level_entry_fields
    success_url = reverse_lazy("taxonomies:adminstrative_region_level_list")

    def form_valid(self, form):
        messages.success(self.request, "The administrative region level was updated successfully.")
        return super(AdministrativeRegionLevelUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The administrative region level was not updated successfully.")
        form.error_css_class = "error"
        return super(AdministrativeRegionLevelCreate, self).form_invalid(form)


class AdministrativeRegionLevelDelete(DeleteView):
    template_name_suffix = "_delete_form"
    model = AdministrativeRegionLevel
    success_url = reverse_lazy("taxonomies:adminstrative_region_level_list")

    def form_valid(self, form):
        messages.success(self.request, "The administrative region level was deleted successfully.")
        return super(AdministrativeRegionLevelDelete, self).form_valid(form)


adminstrative_region_entry_fields = [
    "id",
    "title",
    "administrative_region_level",
    "parent_administrative_region",
]


class AdministrativeRegionList(FilterView):
    template_name_suffix = "_list"
    model = AdministrativeRegion
    paginate_by = 15
    ordering = ["id"]
    filterset_fields = {
        "id": ["exact"],
        "title": ["icontains"],
        "administrative_region_level": ["exact"],
        "parent_administrative_region": ["exact"],
    }

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


class AdministrativeRegionCreate(CreateView):
    template_name_suffix = "_create_form"
    model = AdministrativeRegion
    fields = adminstrative_region_entry_fields
    success_url = reverse_lazy("taxonomies:adminstrative_region_list")

    def form_valid(self, form):
        messages.success(self.request, "The administrative region was created successfully.")
        return super(AdministrativeRegionCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The administrative region was not created successfully.")
        form.error_css_class = "error"
        return super(AdministrativeRegionCreate, self).form_invalid(form)


class AdministrativeRegionUpdate(UpdateView):
    template_name_suffix = "_update_form"
    model = AdministrativeRegion
    fields = adminstrative_region_entry_fields
    success_url = reverse_lazy("taxonomies:adminstrative_region_list")

    def form_valid(self, form):
        messages.success(self.request, "The administrative region was updated successfully.")
        return super(AdministrativeRegionUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The administrative region was not updated successfully.")
        form.error_css_class = "error"
        return super(AdministrativeRegionUpdate, self).form_invalid(form)


class AdministrativeRegionDelete(DeleteView):
    template_name_suffix = "_delete_form"
    model = AdministrativeRegion
    success_url = reverse_lazy("taxonomies:adminstrative_region_list")

    def form_valid(self, form):
        messages.success(self.request, "The administrative region was deleted successfully.")
        return super(AdministrativeRegionDelete, self).form_valid(form)
