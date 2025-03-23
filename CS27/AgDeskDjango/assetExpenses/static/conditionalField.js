// Actions
function enableMaintenanceField() {
    const maintenanceDiv = document.getElementById("div_id_MaintenanceID");
    maintenanceDiv.hidden = false;
}

function disableMaintenanceField() {
    const maintenanceDiv = document.getElementById("div_id_MaintenanceID");
    maintenanceDiv.hidden = true;

    const maintenanceSelect = document.getElementById("id_MaintenanceID");
    maintenanceSelect.value = maintenanceSelect.options[0];
}


// Controller
function expenseTypeChanged() {
    const expenseTypeSelect = document.getElementById("id_expenseType");
    const newType = expenseTypeSelect.value;
    if (newType == 1) { // 1 = Maintenance
        enableMaintenanceField();
    } else {
        disableMaintenanceField();
    }
}


// Events
document.addEventListener('DOMContentLoaded', function() {
    const expenseTypeSelect = document.getElementById("id_expenseType");
    expenseTypeSelect.addEventListener("change", expenseTypeChanged);

    // Initialise
    expenseTypeChanged();
});
