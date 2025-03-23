$(document).ready(function() {
    initializeDashboard();
    setupEventListeners();
});

function initializeDashboard() {
    $.ajax({
        url: '/getLayout',
        type: 'GET',
        success: function(response) {
            console.log('Layout data retrieved:', response);
            if (response.layout && response.widgets) {
                window.dashboard = renderDashboardLayout(response.layout, response.widgets);
            } else {
                console.log('No saved layout found:', response.message);
                
            }
            console.log('Dashboard initialized:', window.dashboard);
            disableEditMode(window.dashboard.grid.api);
        },
        error: function(xhr, status, error) {
            console.error('Failed to retrieve layout', error);
        }
    });
}

function toggleEditMode() {
    if (!dashboard || !dashboard.grid || !dashboard.grid.api) {
        console.error('Dashboard or grid.api is not defined');
        return;
    }

    var gridster = dashboard.grid.api;
    if (typeof gridster.enable !== 'function' || typeof gridster.disable !== 'function') {
        console.error('Gridster does not have enable/disable methods');
        return;
    }

    if (gridster.isEnabled) {
        disableEditMode(gridster);
    } else {
        enableEditMode(gridster);
    }
}

function enableEditMode(gridster) {
    gridster.enable();
    $('#enable-drag').text('Save');
    gridster.isEnabled = true;
    $('#add-widget').css({
        'display': 'inline-block',
        'visibility': 'visible'
    });
    $('.gridster li').append('<span class="widget-delete-btn" style="display:none;">×</span>');
    $('.widget-delete-btn').show();
}

function disableEditMode(gridster) {
    gridster.disable();
    $('#enable-drag').text('Edit');
    gridster.isEnabled = false;
    $('#add-widget').css({
        'display': 'none',
        'visibility': 'hidden'
    });
    $('.widget-delete-btn').hide();
    saveDashboardLayout();
}

function saveDashboardLayout() {
    var layout = [];
    var widgets = [];

    $('.gridster > ul > li').each(function(index) {
        var $this = $(this);
        var widgetID = $this.attr('id');
        if (widgetID) {
            widgetId = widgetID.replace('widget-', '');
        } else {
            console.error('Widget ID is not defined for element:', $this);
            return;
        }

        layout.push({
            "html": this.outerHTML,
            "col": $this.attr('data-col'),
            "row": $this.attr('data-row'),
            "sizex": $this.attr('data-sizex'),
            "sizey": $this.attr('data-sizey')
        });

        var widgetScope;
        for (var i = 0; i < window.dashboard.activeWidgets.length; i++) {
            if (window.dashboard.activeWidgets[i].__widget__.id === widgetID) {
            widgetScope = window.dashboard.activeWidgets[i].scope;
            break;
            }
        }
        widgets.push({
            "id": widgetId,
            "col": $this.attr('data-col'),
            "row": $this.attr('data-row'),
            "sizex": $this.attr('data-sizex'),
            "sizey": $this.attr('data-sizey'),
            "scope": widgetScope
        });
    });

    $.ajax({
        url: '/saveLayout',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ layout: layout, widgets: widgets }),
        success: function(response) {
            console.log('Layout saved successfully');
        },
        error: function(xhr, status, error) {
            console.error('Failed to save layout', error);
        }
    });
}

function renderDashboardLayout(layout_data, widgets_data) {
    var dashboardContainer = document.getElementById('CentralPage');
    var dashboard = new Dashboard({viewportWidth: dashboardContainer.offsetWidth, viewportHeight: dashboardContainer.offsetHeight, name: 'dashboard',
                                    widgetBaseDimensions: [320, 340], widgetMargins: [5,5]
                                    });
    var gridster = dashboard.grid.api;
    dashboard.hide()
    setTimeout(() => {dashboard.show()}, 300); // Used to hide animations while the widgets rearrange themselves
    widgets_data.forEach(function(widget) {
        dashboard.addWidget(widget.name, widget.type, {
            col: widget.sizex,
            row: widget.sizey,
            scope: widget.scope
        });

    widgetElement = gridster.$widgets[gridster.$widgets.length - 1];
    widgetElement.setAttribute('data-col', widget.col);
    widgetElement.setAttribute('data-row', widget.row);
    widgetElement.id = ('widget-' + widget.id);

    // Update priority classes for MyTasks widget
    if (widget.type === 'myTasks') {
        // Immediate update
        setTimeout(() => {
            updatePriorityClasses(widgetElement);
        }, 0);

        // Create a MutationObserver instance
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    updatePriorityClasses(widgetElement);
                }
            });
        });
        // Configuration of the observer:
        var config = { childList: true, subtree: true };

        // Start observing the target node for configured mutations
        observer.observe(widgetElement, config);
    }});

    gridster.update_widget_position(gridster.$widgets);
    gridster.disable();
    return dashboard;
}

function updatePriorityClasses(widgetElement) {
    var prioritySpans = widgetElement.querySelectorAll('.priority-indicator');
    prioritySpans.forEach(span => {
        var priority = span.textContent.trim().toLowerCase();
        if (!priority) {
            // If textContent is empty, use the stored priority
            priority = span.getAttribute('data-priority');
        } else {
            // Store the priority as a data attribute
            span.setAttribute('data-priority', priority);
        }

        // Clear the text content
        span.textContent = '';
        if (priority) {
            // Add the priority class and a general 'priority-circle' class
            span.className = `priority-indicator priority-circle ${priority}-priority`;
        }
    });
}

function setupEventListeners() {
    $('#enable-drag').click(toggleEditMode);
    $('#add-widget-form').on('submit', handleSaveNewWidget);
    $(document).on('click', '.widget-delete-btn', handleDeleteWidget);

     // Add event listener for date change in MyTasks widget
    $(document).on('change', '#myTasks-date-input', function() {
        var date = $(this).val();
        var widgetID = $(this).closest('.widget-myTasks').attr('id');
        updateMyTasksWidget(date , widgetID);
    });

    // Add event listener for check-in button in MyCheckouts widget
    $(document).on('click', '.check-in-btn', handleCheckInClick);
    $('#confirmCheckin').on('click', handleCheckInSubmit);
}

function updateMyTasksWidget(date, widgetId) {
    $.ajax({
        url: '/update_my_tasks/',
        type: 'POST',
        data: {
            date: date,
            csrfmiddlewaretoken: getCookie('csrftoken'),
            id: (widgetId.split('-')[1]),
        },
        success: function(response) {
            if (response.success) {
                // Find the MyTasks widget and update its content
                var myTasksWidget = $('.gridster .widget-myTasks');
                if (myTasksWidget.length) {
                    var widgetContent = myTasksWidget.find('tbody');
                    widgetContent.empty();
                    
                    // Rebuild the task list with the new data
                    response.data.forEach(function(task) {
                        var taskItem = $('<tr>');
                        taskItem.append($('<td>').text(task.label));
                        taskItem.append($('<td>').text(task.value.status));
                        taskItem.append($('<td>').append($('<span>').addClass('priority-indicator priority-circle ' + task.value.priority + '-priority')));
                        widgetContent.append(taskItem);
                    });
                }
            } else {
                console.error('Failed to update MyTasks widget:', response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error updating MyTasks widget:', error);
        }
    });
}

// Helper function to get CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handleSaveNewWidget(event) {
    event.preventDefault();  // Prevent the default form submission
    var gridster = dashboard.grid.api;
    var form = $(this);  // 'this' refers to the form that triggered the event
    var formData = new FormData(form[0]);

    $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'  // Explicitly set this header
        },
        success: function(response) {
            console.log('New widget saved:', response.widget.name);
            dashboard.addWidget(response.widget.name, response.widget.type, {col: response.widget.sizex,
                row: response.widget.sizey, scope:response.widget.scope});
            
            // add DB widget ID to the element
            widgetElement = gridster.$widgets[gridster.$widgets.length - 1];
            widgetElement.id = ('widget-' + response.widget.id);

            // Optionally, close the modal if it exists
            $('#addWidget').modal('hide');
        },
        error: function(xhr, status, error) {
            console.error('Failed to save new widget', error);
            // Optionally, display an error message to the user
        }
    });
}

function handleDeleteWidget(event) {
    event.stopPropagation();
    var widgetElement = $(this).parent()[0];
    var gridster = window.dashboard.grid.api;

    var widgetId = widgetElement.id;
    if (widgetId) {
        widgetId = widgetId.replace('widget-', '');
    } else {
        console.error('Widget ID is not defined for element:', widgetElement);
        return;
    }

    if (confirm('Are you sure you want to delete this widget?')) {
        $.ajax({
            url: '/deleteWidget',
            type: 'POST',
            data: { widget_id: widgetId },
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    gridster.remove_widget(widgetElement);
                    delete window.dashboard.widgets[widgetId];
                    saveDashboardLayout();
                } else {
                    console.error('Failed to delete widget:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error deleting widget:', error);
            }
        });
    }
}

function handleCheckInClick(event) {
    var logID = $(this).data('log-id');
    var assetName = $(this).data('asset-name');

    $('#checkin').modal('show');
    $('#checkin #logID').val(logID);
    $('#checkin #modalTitle').text('Check In: ' + assetName);
}

function handleCheckInSubmit() {
    var logID = $('#checkin #logID').val();
    var notes = $('#checkin #notes').val();

    $.ajax({
        url: '/dashboard/checkin/',
        type: 'POST',
        data: {
            logID: logID,
            notes: notes,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success: function(response) {
            if (response.success) {
                $('#checkin').modal('hide');
                updateMyCheckoutsWidget();
            } else {
                console.error('Failed to check in:', response.error);
                // Display error message to user
            }
        },
        error: function(xhr, status, error) {
            console.error('Error checking in:', error);
            // Display error message to user
        }
    });
}

function updateMyCheckoutsWidget() {
    $.ajax({
        url: '/dashboard/get_my_checkouts/',
        type: 'GET',
        success: function(response) {
            if (response.success) {
                var myCheckoutsWidget = $('.widget-myCheckouts');
                if (myCheckoutsWidget.length) {
                    var widgetContent = myCheckoutsWidget.find('tbody');
                    widgetContent.empty();
                    
                    response.data.forEach(function(checkout) {
                        var checkoutItem = $('<tr>');
                        checkoutItem.append($('<td>').text(checkout.label));
                        checkoutItem.append($('<td>').text(checkout.value.startTime));
                        var checkInButton = $('<button>')
                            .addClass('btn btn-primary check-in-btn')
                            .attr('data-log-id', checkout.value.logID)
                            .attr('data-asset-name', checkout.label)
                            .text('Check In');
                        checkoutItem.append($('<td>').append(checkInButton));
                        widgetContent.append(checkoutItem);
                    });
                }
            } else {
                console.error('Failed to update MyCheckouts widget:', response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error updating MyCheckouts widget:', error);
        }
    });
}
