from UserAuth.models import UserProfile
from FarmAcc.models import FarmInfo

def current_user_context(request):
    try:
        current_user = UserProfile.objects.get(id=request.user.id)
        username = current_user.username
        firstName = current_user.first_name
        lastName = current_user.last_name
        if current_user.currentFarm_id is None:
            farmName = "No Farm Assigned"
            current_user.currentFarm_id = 0
            currentFarmID = 0
        else:
            currentFarmID = current_user.currentFarm_id
            farmName = FarmInfo.objects.get(id = currentFarmID).farm_name

        context = {
            "username": username,
            "firstName": firstName,
            "lastName": lastName,
            "farmName": farmName,
            "currentFarmID": currentFarmID
        }
        return context

    except UserProfile.DoesNotExist: 
        return {
            "currentFarmID": 0
        }
    