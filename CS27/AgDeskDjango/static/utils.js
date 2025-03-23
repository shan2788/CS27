function go_to_asset_url(assetCategory, assetID, type, maintenanceID = null, damageID = null, expenseID = null){
    if (maintenanceID != null){
        console.log("yes");
        window.location.href = `${type}/${maintenanceID}/details`;
    }
    else if (damageID != null){
        window.location.href = `${type}/${damageID}/details`;
    }
    else if (expenseID != null){
        window.location.href = `${type}/${expenseID}/details`;
    }
    else
    {
        window.location.href = `/asset/${assetCategory}/${assetID}/${type}`;
    }
    
}

function go_to_user_management_url(userID){
    window.location.href = `/settings/userDetails/${userID}`;
}

function go_to_team_url(teamID){
    window.location.href = `/settings/update-team/${teamID}`;
}

function go_to_file_url(fileID){
    window.location.href = `/farm/file-details/${fileID}`;
}
