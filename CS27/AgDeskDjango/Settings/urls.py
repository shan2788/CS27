"""
URLs for the settings pages.
"""


# Imports
from django.urls import path
from . import views


# Patterns
urlpatterns = [
    path("farm"                             , views.farmSettings  , name="farmSettings"   ),
    path("team_settings"                    , views.teamSettings  , name="team_settings"  ),
    path("update-team/<int:team_id>/"       , views.teamDetails   , name="team_details"   ),
    path("deleteTeam/<int:team_id>"         , views.deleteTeam    , name="delete_team"    ),
    path("userManagement"                   , views.userManagement, name="user_management"),
    path("userDetails/<int:user_id>"        , views.userDetails   , name="user_details"   ),
    path("profile"                          , views.profileUpdate , name="profileUpdate"  ),
    path("generateCode"                     , views.generate_code , name="generate_code"  ),
    path("profile/manage-farms"             , views.manage_farms  , name="manage_farms"   ),
    path("profile/switch-farm/<int:farm_id>", views.switch_farm   , name="switch_farm"    ),
    path("profile/remove-farm/<int:farm_id>", views.remove_farm   , name="remove_farm"    )
]
