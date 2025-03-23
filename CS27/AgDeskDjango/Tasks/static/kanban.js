// Dragging functionality
const drag = (event) => {
    event.dataTransfer.setData("text/plain", event.target.id);
    $('.dropzone').addClass('droppable-hint');
}

const allowDrop = (ev) => {
    ev.preventDefault();
    if (hasClass(ev.target, "dropzone")) {
        addClass(ev.target, "droppable");
    }
}

const clearDrop = (ev) => {
    removeClass(ev.target, "droppable");
}

const drop = (event) => {
    event.preventDefault();
    const data = event.dataTransfer.getData("text/plain");
    const element = document.querySelector(`#${data}`);
    try {
        // remove the spacer content from dropzone
        event.target.removeChild(event.target.firstChild);
        // add the draggable content
        event.target.appendChild(element);
        // remove the dropzone parent
        unwrap(event.target);
        // I think this is the right place? The function isn't actually checking for board differences anyway.
        enableSaveBtn();
    } catch (error) {
        console.warn("can't move the item to the same place");
    }
}

const dragEnd = () => {
    updateDropzones();
}

const updateDropzones = () => {
    // Reset all the dropzones
    var dz = $('<div class="dropzone rounded" ondrop="drop(event)" ondragover="allowDrop(event)" ondragleave="clearDrop(event)"> &nbsp; </div>');
    $('.dropzone').remove();
    dz.insertAfter('.dropzone-location');
}

// helpers
function hasClass(target, className) {
    return new RegExp('(\\s|^)' + className + '(\\s|$)').test(target.className);
}

function addClass(ele, cls) {
    if (!hasClass(ele, cls)) ele.className += " " + cls;
}

function removeClass(ele, cls) {
    if (hasClass(ele, cls)) {
        var reg = new RegExp('(\\s|^)' + cls + '(\\s|$)');
        ele.className = ele.className.replace(reg, ' ');
    }
}

function unwrap(node) {
    node.replaceWith(...node.childNodes);
}


// Remove a card
function removeCard(event) {
    const btn = window.event.srcElement;
    let card  = btn.parentElement;
    while (!card.classList.contains("card")) {
        card = card.parentElement;
    }

    // Adding back to the add task modal
    addCardToAddTaskModal(card)

    // Actuall remove the card
    card.remove();
    updateDropzones();
    enableSaveBtn();
}


// Adding a task back to the add task modal from its card element
function addCardToAddTaskModal(card) {
    // Get the card data
    const status      = getCardStatus(card);
    const taskID      = card.dataset.taskId;
    const name        = card.querySelector(".task-name"       ).innerHTML;
    const description = card.querySelector(".task-desc"       ).innerHTML;
    const dueDate     = card.querySelector(".task-due-date"   ).innerHTML;
    const assignedTo  = card.querySelector(".task-assigned-to").innerHTML;

    // Assemble data into formats
    const value       = `${status}, -1, ${taskID}, '${assignedTo}', '${dueDate}', '${name}', '${description}'`;
    const displayText = `${name} - ${assignedTo} - ${dueDate}`;

    // Add select option
    const select     = document.getElementById("add-task-select");
    const option     = document.createElement("option");
    option.id        = `add-task-option-${taskID}`;
    option.value     = value;
    option.innerHTML = displayText;
    select.appendChild(option);

    updateAddTaskModal();
}


// Finding the status number of a given card element
function getCardStatus(card) {
    bucketCol = card.parentElement;
    while (!bucketCol.classList.contains("bucket-col")) {
        bucketCol = bucketCol.parentElement;
    }
    bucketName = bucketCol.getElementsByClassName("bucket-name")[0].innerHTML;
    bucketsContainer = document.getElementById("buckets-container");
    for (let i = 0; i < bucketsContainer.children.length; i++) {
        if (bucketsContainer.children[i].getElementsByClassName("bucket-name")[0].innerHTML == bucketName) {
            return i;
        }
    }
    return -1;
}


// Changing visibility in the add task modal
function updateAddTaskModal() {
    const select = document.getElementById("add-task-select");
    const addBtn = document.getElementById("add-task-btn"   );
    const msg    = document.getElementById("no-tasks-msg"   );

    if (select.children.length) {
        select.hidden = false;
        addBtn.hidden = false;
        msg.hidden    = true;
    } else {
        select.hidden = true;
        addBtn.hidden = true;
        msg.hidden    = false;
    }
}


// Saving the kanban board
function enableSaveBtn() {
    saveBoardBtn = document.getElementById("save-board-btn");
    saveBoardBtn.style.backgroundColor = "darkgreen";

    saveBoardBtn.removeEventListener("click", noChangedMessage);
    saveBoardBtn.addEventListener(   "click", saveBoard       );

    window.addEventListener("beforeunload", unsavedConfirmation);
}

function disableSaveBtn() {
    saveBoardBtn = document.getElementById("save-board-btn");
    saveBoardBtn.style.backgroundColor = "darkred";

    saveBoardBtn.removeEventListener("click", saveBoard       );
    saveBoardBtn.addEventListener(   "click", noChangedMessage);

    window.removeEventListener("beforeunload", unsavedConfirmation);
}

// Confirm before discard unsaved changes
function unsavedConfirmation(e) {
    e.preventDefault();
    e.returnValue = '';
}

// Message for unchanged board
function noChangedMessage(e) {
    const fakeResponse = {
        "status" : "info"                  ,
        "message": "No changes to be saved"
    };
    displayMessage(fakeResponse);
}

function saveBoard(e) {
    e.preventDefault();

    let cards      = [];
    let allBuckets = document.getElementsByClassName("bucket-container");

    for (let status = 0; status < allBuckets.length; status++) {
        let bucket = allBuckets[status].children
        let order  = 0;
        for (let i = 0; i < bucket.length; i++) {
            if (hasClass(bucket[i], "card")) {
                cards.push({
                    "taskID": parseInt(bucket[i].dataset.taskId),
                    "status": parseInt(status                  ),
                    "order" : parseInt(order                   )
                })
                order++;
            }
        }
    }

    let csrf = document.getElementById("csrf-hiding-spot").getElementsByTagName("input")[0].getAttribute("value");

    $.ajax({
        url    : "/tasks/updateKanban",
        type   : "POST"               ,
        data   : {
            cards: JSON.stringify(cards),
            csrfmiddlewaretoken: csrf
        },
        success: (response) => {
            displayMessage(response);
            disableSaveBtn();
        },
        error  : (xhr) => {
            const response = JSON.parse(xhr.responseText);
            displayMessage(response);
        }
    });
}


// Function for displaying messages, intended for saveBoard callback
function displayMessage(response) {
    const messageBox     = document.getElementById("message-box");
    if (response.status == "error") {response.status = "danger"}
    messageBox.className = `alert alert-${response.status}`;
    messageBox.innerHTML = response.message;
    messageBox.hidden    = false;
}


// Buttons
document.addEventListener("DOMContentLoaded", function() {
    // Initialise kanban board
    const startingDataElem = $("#starting-data")[0];
    const startingData     = startingDataElem.dataset.cardsData;
    if (startingData.length > 2) {
        const cardList = startingData.slice(2, -2).split("), (");
        for (let i = 0; i < cardList.length; i++) {
            addCard(cardList[i]);
        }
    }
    startingDataElem.remove();
    updateDropzones();


    // Adding cards
    function addCard(cardData) {
        let cardDataList = cardData.split(", "); // Convert to list
        // Remove quotes from strings
        for (let i = 3; i < 7; i++) {
            cardDataList[i] = cardDataList[i].slice(1, -1);
        }

        // Generate template
        let template = document.getElementById("task-card-template");
        let card = template.content.cloneNode(true);

        // Fill in template
        card.querySelector(".card"            ).id             = `card_${cardDataList[2]}`;
        card.querySelector(".card"            ).dataset.taskId = cardDataList[2];
        card.querySelector(".task-name"       ).innerHTML      = cardDataList[5];
        card.querySelector(".task-desc"       ).innerHTML      = cardDataList[6];
        card.querySelector(".task-due-date"   ).innerHTML      = `Due Date: ${cardDataList[4]}`;
        card.querySelector(".task-assigned-to").innerHTML      = `Assigned To: ${cardDataList[3]}`;

        // Place template
        let bucket = document.getElementsByClassName("bucket-container")[cardDataList[0]];
        bucket.appendChild(card);
    }


    // Open the add task modal
    let addTaskModalBtn = document.getElementById("add-task-modal-btn");
    addTaskModalBtn.addEventListener("click", openAddTaskModal);

    function openAddTaskModal(e) {
        e.preventDefault();
        $("#add-task-modal").modal("show");
    }


    // Actually adding the task
    let addTaskBtn = document.querySelector("#add-task-btn");
    if (addTaskBtn) { // Check if the button exists, won't exist if there's no unused tasks
        addTaskBtn.addEventListener("click", addTask);
    }

    function addTask(e) {
        e.preventDefault();

        const select = document.getElementById("add-task-select");
        let cardData = select.value;
        let cardDataList = cardData.split(", ");
        $(`#add-task-option-${cardDataList[2]}`).remove();

        addCard(cardData);
        updateDropzones();
        updateAddTaskModal();
        enableSaveBtn();
    }


    // Save button starts out disabled
    disableSaveBtn();
});
