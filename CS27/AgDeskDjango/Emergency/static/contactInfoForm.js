document.addEventListener("DOMContentLoaded", function() {
    // Constants
    let contactInfoForms = document.querySelectorAll(".contact-info-form");
    let container = document.querySelector("#contact-info-forms");
    let addButton = document.querySelector("#add-form");
    let totalForms = document.querySelector("#id_contactInfo-TOTAL_FORMS");

    // Setup
    let formNum = contactInfoForms.length - 1;
    addButton.addEventListener("click", addForm);

    makeRequired(container.children[0]);

    // Functions
    function makeRequired(childForm) {
        const selectElement = childForm.children[1].children[1].children[0];
        selectElement.required = true;
    }

    function addForm(e) {
        e.preventDefault();

        let newForm = contactInfoForms[0].cloneNode(true);

        let formRegex = new RegExp(`contactInfo-(\\d){1}-`, 'g'); // At most 10 fields

        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `contactInfo-${formNum}-`);

        // Update the names and ids of the cloned form fields
        updateInfoFormFields(newForm, formNum, formRegex);

        // Add delete button functionality
        // More duplicate code
        let deleteButton = newForm.querySelector(".delete-form");
        deleteButton.addEventListener("click", function() {
            newForm.remove();
            updateTotalForms();
            updateInfoFormIndexes();
        });

        makeRequired(newForm);

        container.appendChild(newForm);
        updateTotalForms();
    }

    function updateInfoFormFields(form, index, regex) {
        let newFields = form.querySelectorAll("input, select, textarea");

        newFields.forEach(function(field) {
            let name = field.getAttribute("name");
            if (name) { // Validation?
                name = name.replace(regex, `contactInfo-${index}-`);
                field.setAttribute("name", name);
            }

            let id = field.getAttribute("id");
            if (id) {
                id = id.replace(regex, `contactInfo-${index}-`);
                field.setAttribute("id", id);
            }
        });
    }

    function updateTotalForms() {
        let currentForms = document.querySelectorAll(".contact-info-form").length;
        totalForms.setAttribute("value", `${currentForms}`);
    }

    // The formset MUST have consecutive indexes
    function updateInfoFormIndexes() {
        let currentForms = document.querySelectorAll(".contact-info-form");
        let formRegex = new RegExp(`contactInfo-(\\d){1}-`, 'g');
        let index = 0;

        currentForms.forEach(function(form) {
            updateInfoFormFields(form, index, formRegex);
            index += 1;
        });
    }

    // Add delete functionality to existing forms
    contactInfoForms.forEach(function(form) {
        let deleteButton = form.querySelector(".delete-form");
        deleteButton.addEventListener("click", function() {
            form.remove();
            updateTotalForms();
            updateInfoFormIndexes();
        });
    });
})
