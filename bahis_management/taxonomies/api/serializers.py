from bahis_management.taxonomies.models import (
    AdministrativeRegion,
    AdministrativeRegionLevel,
    Taxonomy,
)
from rest_framework import serializers


class TaxonomySerializer(serializers.ModelSerializer):
    csv_file_stub = serializers.FileField(use_url=False, read_only=True, source="csv_file")

    class Meta:
        model = Taxonomy
        fields = ["id", "title", "slug", "csv_file", "csv_file_stub"]


class AdministrativeRegionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeRegionLevel
        fields = ["id", "title"]


class AdministrativeRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeRegion
        fields = [
            "id",
            "title",
            "administrative_region_level",
            "parent_administrative_region",
        ]
