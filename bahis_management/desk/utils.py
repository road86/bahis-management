import requests
from rest_framework.authtoken.models import Token

from bahis_management.desk.models import Module
from config.settings.base import env


# get assets list for authenticated user
def get_assets_for_user(request):
    api_url = env("KOBOTOOLBOX_KF_API_URL")
    token = Token.objects.get(user=request.user).key
    response = requests.get(f"{api_url}assets/?format=json", headers={"Authorization": f"Token {token}"})
    asset_list = response.json().get("results")
    return asset_list


# get module for authenticated user
def get_modules_for_user(request):
    asset_list = get_assets_for_user(request)

    if asset_list:
        asset_id_list = tuple([asset.get("uid") for asset in asset_list if asset.get("has_deployment", False)])

        return Module.objects.raw(
            f"""
                                WITH RECURSIVE module(id) AS (SELECT *
                                            FROM desk_module
                                            WHERE form in ({', '.join("'" + str(id) + "'" for id in asset_id_list)})
                                            UNION ALL
                                            SELECT dm.*
                                            FROM desk_module AS dm,
                                                 module AS m
                                            WHERE dm.id = m.parent_module_id)
                                SELECT *
                                FROM module order by parent_module_id, sort_order
                                """
        )
