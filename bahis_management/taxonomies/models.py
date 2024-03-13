from django.db import models
from django.template.defaultfilters import slugify


def validate_file_is_csv(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension - only CSV files are supported,')


class Taxonomy(models.Model):
    """
    This model is used to define any custom taxonomies.
    """

    title = models.CharField(
        max_length=150,
        help_text="The human-readable title for the taxonomy, e.g. Disease List",
    )
    slug = models.SlugField(
        unique=True,
        help_text="The machine-readable name for the taxonomy, e.g. disease-list",
    )
    csv_file = models.FileField(
        upload_to="taxonomies",
        validators=[validate_file_is_csv],
        help_text="The CSV file containing the taxonomy data, taxonomies should meet the XLSForm Choices specification",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # We use underscores for our slugs because that is consistent with what the XLSForms use
        self.slug = slugify(self.title).replace("-", "_")
        super(Taxonomy, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class AdministrativeRegionLevel(models.Model):
    """
    This model is used to define the only compulsory taxonomy: administrative regions.
    Administrative regions / units / divisions, subnational entities, or constituent states
    (as well as many similar generic terms) are geographical areas into which a state is divided.
    This model is used to define the administrative region levels.
    """

    id = models.IntegerField(
        primary_key=True,
        help_text="The region level identifier, e.g. 1 for state, 2 for district, etc.",
    )
    title = models.CharField(
        max_length=150,
        help_text="The title for the administrative region level, e.g. District",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AdministrativeRegion(models.Model):
    """
    This model is used to define the only compulsory taxonomy: administrative regions.
    Administrative regions / units / divisions, subnational entities, or a constituent states
    (as well as many similar generic terms) are geographical areas into which a state is divided.
    This model is used to define the administrative regions for a country.
    """

    id = models.PositiveBigIntegerField(
        primary_key=True,
        help_text="The heirarchical identifier for the administrative region level, e.g. a level 1 geography may have an id of 01, and a level 2 geography may have an id of 01001",
    )
    title = models.CharField(
        max_length=150,
        help_text="The name of the region",
    )
    administrative_region_level = models.ForeignKey(
        AdministrativeRegionLevel,
        on_delete=models.CASCADE,
        help_text="The region administrative level",
    )
    parent_administrative_region = models.ForeignKey(
        "AdministrativeRegion",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The parent region of this region (leave blank for top level regions)",
    )
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
