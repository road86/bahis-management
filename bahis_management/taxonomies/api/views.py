from rest_framework import parsers, permissions, response, status, views, viewsets

from bahis_management.taxonomies.api.serializers import (
    AdministrativeRegionLevelSerializer,
    AdministrativeRegionSerializer,
    TaxonomySerializer,
)
from bahis_management.taxonomies.models import AdministrativeRegion, AdministrativeRegionLevel, Taxonomy


class TaxonomyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom Taxonomies to be viewed or edited.
    """

    queryset = Taxonomy.objects.all().order_by("slug")
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    serializer_class = TaxonomySerializer
    permission_classes = [permissions.AllowAny]  # [permissions.IsAuthenticated] FIXME auth is turned off


class AdministrativeRegionLevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AdministrativeRegionLevels to be viewed or edited.
    """

    queryset = AdministrativeRegionLevel.objects.all().order_by("id")
    serializer_class = AdministrativeRegionLevelSerializer
    permission_classes = [permissions.AllowAny]  # [permissions.IsAuthenticated] FIXME auth is turned off


class AdministrativeRegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AdministrativeRegions to be viewed or edited.
    """

    queryset = AdministrativeRegion.objects.all().order_by("id")
    serializer_class = AdministrativeRegionSerializer
    permission_classes = [permissions.AllowAny]  # [permissions.IsAuthenticated] FIXME auth is turned off


class AdministrativeRegionCatchmentView(views.APIView):
    """
    This is a specific API endpoint that gets a "catchment".
    A catchment is defined as all children regions and the direct
    line of parents up to the top level.
    """

    permission_classes = [permissions.AllowAny]  # [permissions.IsAuthenticated] FIXME auth is turned off

    def get(self, request, format=None):
        """
        Return catchment
        """
        serializer = AdministrativeRegionSerializer

        def get_direct_parent(region_id):
            parent = AdministrativeRegion.objects.get(id=region_id).parent_administrative_region
            if parent is None:
                return []
            else:
                return [parent] + get_direct_parent(parent.id)

        def get_all_children(region_id):
            children = AdministrativeRegion.objects.filter(parent_administrative_region=region_id)
            if len(children) == 0:
                return []
            else:
                all_children = []
                for child in children:
                    all_children.append(child)
                    all_children.extend(get_all_children(child.id))
                return all_children

        region_id = request.query_params.get("id", None)
        if region_id is None:
            return response.Response("No region id provided", status=status.HTTP_400_BAD_REQUEST)
        else:
            region = AdministrativeRegion.objects.get(id=int(region_id))
            direct_parents = get_direct_parent(region.id)
            all_children = get_all_children(region.id)
            print(type(all_children))
            print(len(all_children))
            print(type(all_children[0]))
            print(serializer(all_children[0]).data)
            return response.Response(
                serializer([region] + direct_parents + all_children, many=True).data, status=status.HTTP_200_OK
            )
