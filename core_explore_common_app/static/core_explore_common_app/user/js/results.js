/**
 * Get data sources results html holders
 */
var getDataSourcesResultsHTML = function() {
    var query_id = $("#query_id").html();
    updateKeywordForm(data_sorting_fields);
    $.ajax({
        url: getDataSourcesHTMLUrl,
        type: "GET",
        data: {
            'query_id': query_id
        },
        success: function(data) {
            var $results = $("#results");
            $results.html(data.results);
            getDataSourcesResults();
            initFilter();
        },
        error: function(data) { }
    });
};



/**
 * Init the sorting binding structure and the listener
 */
var initFilter = function() {

    /**
     * Create the binding structure with the default setting given by the backend and the available
     * sorting fields in the HTML template.
     **/
    var dropdownMenuElement = $(".filter-dropdown-menu")[0];
    try {
        if (dropdownMenuElement) {

            var dropdownMenuElementChildren = dropdownMenuElement.children;

            if (dropdownMenuElementChildren && dropdownMenuElementChildren.length > 0) {

                // Retrive data from the KeywordForm if it is available
                var order_by_field_elt = $("#id_order_by_field");
                if (order_by_field_elt.val() && order_by_field_elt.val() != '')
                    data_sorting_fields = order_by_field_elt.val().split(',');

                for (var i = 0; i < dropdownMenuElementChildren.length; ++i) {
                    var isFoundMatch = false;
                    var currentDropdownFieldName = dropdownMenuElementChildren[i].id.replace('sort_', '');

                    // Looking for missing fields in the data_sorting_fields table
                    data_sorting_fields.forEach(function(dataSortingItem, j) {
                        // clean empty field
                        if (dataSortingItem === '') data_sorting_fields.splice(j, 1);
                        if (dataSortingItem.indexOf(currentDropdownFieldName) != -1)
                            isFoundMatch = true;
                    });

                    // if this field is missing, add it without ordering
                    if (!isFoundMatch)
                        data_sorting_fields.push(currentDropdownFieldName);
                }

                // Refresh GUI
                refreshFilterPanel();

                // Add listeners
                $(".filter-dropdown-menu li").click(function(event) {
                    toggleFilter(event);
                });

            } else {
                throw ("Could not find the sorting fields in the HTML template.");
            }


        } else {
            throw ("HTML template malformed");
        }
    } catch (error) {
        console.error("Error: Something went wrong initializing sorting fields ", error);
    }
}


/**
 *  Refresh the filter dropdown in function of the current filter structure state
 */
var refreshFilterPanel = function() {

    data_sorting_fields.forEach(function(field) {
        var current_filter_value = field;
        var ordering_prefix = '';

        if (field[0] === '+' || field[0] === '-') {
            ordering_prefix = field[0];
            current_filter_value = field.slice(1);
        }

        var current_filter_element = $("#sort_" + current_filter_value);

        switch (ordering_prefix) {
            case '':
                current_filter_element.children()[0].className = "fa fa-random"
                break;
            case '+':
                current_filter_element.children()[0].className = "fa fa-sort-alpha-asc"
                break;
            case '-':
                current_filter_element.children()[0].className = "fa fa-sort-alpha-desc"
                break;
            default:
                console.error('Error: Wrong filter format.')
        }
    });

}

/**
 *  Toggle data filter and set the new sort in the sorting structure
 *  @param jQueryClickEvent
 */
var toggleFilter = function(event) {
    // Stop the event propagation to avoid default behavior: close dropdown on click
    event.stopPropagation();
    $('#result-button-filter>i')[0].classList = 'fa fa-spinner fa-spin'
    var clickedButtonElementId = $(event.target).closest('li')[0].id;
    var clickedButtonValue = clickedButtonElementId.replace('sort_', '');

    // update the sorting order in the sorting structure ( ex. ['+title', 'last_modification_date', '-template'] )
    data_sorting_fields.forEach(function(field, index) {
        if (field.indexOf(clickedButtonValue) != -1) {

            if (field[0] === '+') {
                data_sorting_fields[index] = '-' + field.slice(1);
            } else if (field[0] === '-') {
                data_sorting_fields[index] = field.slice(1);
            } else {
                data_sorting_fields[index] = '+' + field;
            }

        }
    });

    // We have updated the sorting order in the sorting structure, then we will update the GUI
    refreshFilterPanel();

    updateKeywordForm(cleanSortingList(data_sorting_fields));
}

/**
 * Remove from the list the non sorted items ( ex. ['+a', 'b', '-c'] => ['+a', '-c'] )
 * @param {Array<string>} inputList
 * @return {Array<string>} cleaned list
 */
var cleanSortingList = function(inputList) {
    var cloneInputList = inputList.slice(0);
    inputList.forEach(function(item) {
        if (item[0] != '+' && item[0] != '-') {
            cloneInputList.forEach(function(cloneItem, index) {
                if (item == cloneItem) cloneInputList.splice(index, 1);
            });
        }
    });
    return cloneInputList;
}

/**
 * When the filter selector it updated, update the hidden form field with the current sorting value
 * @param {Array<string>} order_by_field 
 */
var updateKeywordForm = function(order_by_field) {
    var order_by_field_elt = $("#id_order_by_field");
    if (order_by_field && order_by_field.length >= 0) order_by_field_elt.val(order_by_field.join(','));
}

/**
 * Get data sources results
 */
var getDataSourcesResults = function(order_by_field) {
    var $results = $("#results");

    $results.find(".results-container").each(function() {
        // TODO: check if problem setting variable with async call
        var $result_container = $(this);
        var data_source_url = $result_container.attr("url");
        var result_page = $result_container.find(".results-page");
        get_data_source_results(result_page, data_source_url, order_by_field);
    });
};

/**
 * Get results page
 * @param event
 */
var getResultsPage = function(event) {
    var $target = $(event.target);
    var data_source_url = $target.attr('url');
    var results_page = $target.closest(".results-page");
    get_data_source_results(results_page, data_source_url);
};


/**
 *
 * @param result_page
 * @param data_source_url
 */
var get_data_source_results = function(result_page, data_source_url, order_by_field) {

    $.ajax({
        url: data_source_url,
        type: "GET",
        success: function(data) {
            var nb_results_id = result_page.attr('nb_results_id');
            $("#" + nb_results_id).html(data.nb_results);
            result_page.html(data.results);
            // when the results and the tab are displayed we can init the toggle
            initDisplayDateToggle();
            getDataPermission();
        },
        error: function(data) {
            result_page.html(data.responseText);
        }
    });
};

/*
 * Display the edit icon according to the user permissions
 */
var getDataPermission = function() {

    $("input.input-permission-url").map(function(){
        var inputElement = $(this);
        var data_permission_url = inputElement.attr("value");
        $.ajax({
            url: data_permission_url,
            type: "GET",
            contentType:"application/json; charset=utf-8",
            success: function(data) {
                for(id in data) {
                    if (data[id]) {
                        // show the edit icon
                        var editLinkElement = inputElement.siblings(".permissions-link");
                        editLinkElement.css('display', "inline");
                        // create the click event listener
                        $(editLinkElement).click(function() {
                          openEditRecord(id);
                        });
                    }
                }
            },
            error: function(data) {
                console.log(data)
            }
        });
    });
}

/*
 * Navigate to the edit page with the correct record id
 * @param {string} id of the clicked record
 */
openEditRecord = function(id) {

    $.ajax({
        url : editRecordUrl,
        type : "POST",
        dataType: "json",
        data : {
            "id": id
        },
        success: function(data){
            window.location = data.url;
        },
        error:function(data){
            $.notify("Error while opening the edit page.", {style: 'error'});
        }
    });
};


/*
 * Init the display date toggle
 */
var initDisplayDateToggle = function() {
    // add date toggle listener or delete the toggle
    if (displayLastModificationDate == 'true') {
        // set the checkbox to "checked"
        $('.switch-input').prop('checked', true);
        // create change listener
        $("#date-switch-input").change(function() {
            toggleDate($(this).is(":checked"));
        });
    } else {
        $('#date-toggle').remove();
    }
}

/*
 * Show / Hide the dates on the results list
 * @param: {boolean} value of the checkbox
 */
var toggleDate = function(value) {
    var dateContainers = $('.data-info-right-container');
    if(value) {
        dateContainers.show();
        $( "div[name='result']" ).addClass( "result-line-main-container" )

    } else {
        dateContainers.hide();
        $( "div[name='result']" ).removeClass( "result-line-main-container" )
    }
}


/**
 * Shows/hides a result of the results page
 * @param event
 */
showhideResult = function(event, selector) {
    $(selector).toggle("blind", 500);
    if ($(button).attr("class") == "expand") {
        $(button).attr("class", "collapse");
    } else {
        $(button).attr("class", "expand");
    }
};


/**
 * Load controllers for the results page
 */
$(document).ready(function() {
    getDataSourcesResultsHTML();
});