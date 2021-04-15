// Sorting multi criteria script
SORTING_SUBMIT_DELAY = 3000;
/**
 * Init the sorting binding structure and the listener
 */
var initFilter = function() {

    /**
     * Create the binding structure with the default setting given by the backend and the available
     * sorting fields in the HTML template.
     **/
    var dropdownMenuElement = $(".filter-dropdown-menu:first");
    dataSortingFields = [];
    try {
        if (dropdownMenuElement) {

            var dropdownMenuElementChildren = dropdownMenuElement.children();

            if (dropdownMenuElementChildren && dropdownMenuElementChildren.length > 0) {

                // Retrive data from the KeywordForm if it is available
                var order_by_field_elt = $("#id_order_by_field");
                var filterTable = order_by_field_elt.val().split(';');
                $("a[id*=tab_results_]").each( (index, element)=> {
                    var tabIndex = parseFloat(element.id.replace('tab_results_', ''));

                    // if the index is new and had not been set yet assign the default values
                    if(filterTable[tabIndex] === undefined)
                        filterTable[tabIndex] = defaultDataSortingFields;

                    dataSortingFields[tabIndex] = filterTable[tabIndex].split(',');
                    itemOrder = [];

                    // fill the itemOrder table with the correct order on filter fields ex. ['title', 'date']
                    dropdownMenuElementChildren.each( (dropdownIndex, dropdownElement) => {
                         itemOrder.push($(dropdownElement).attr('data-filter-value'));
                    });

                    // add the order to the fields ex. ['+title', '-date']
                    itemOrder.forEach((orderItemName, itemOrderIndex) => {
                        currentFieldIndex = -1;

                        dataSortingFields[tabIndex].forEach( (field, fieldIndex) =>{
                            if(field.indexOf(orderItemName) > -1)
                                currentFieldIndex = fieldIndex;
                        });

                        if(currentFieldIndex > -1) {
                            itemOrder[itemOrderIndex] = dataSortingFields[tabIndex][currentFieldIndex];
                        }
                    });

                    dataSortingFields[tabIndex] = itemOrder;

                    // Refresh GUI
                    refreshFilterPanel(tabIndex);

                    // create the toggle buttons listeners
                    createSortingListeners();
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
 * When the filter selector it updated, update the hidden form field with the current sorting value
 * @param {Array<string>} order_by_field
 */
var updateKeywordForm = function(order_by_field) {
    var order_by_field_elt = $("#id_order_by_field");
    var inputValue = order_by_field.join(';');

    if (order_by_field && order_by_field.length >= 0) order_by_field_elt.val(inputValue);
}

/**
 *  Refresh the filter dropdown in function of the current filter structure state
 *  @param tabIndex the index of the tab to refresh
 */
var refreshFilterPanel = function(tabIndex) {

    dataSortingFields[tabIndex].forEach(function(field) {
        var current_filter_value = field;
        var ordering_prefix = '';

        if (field[0] === '+' || field[0] === '-') {
            ordering_prefix = field[0];
            current_filter_value = field.slice(1);
        }

        var current_filter_elements = $("#result-button-filter" + tabIndex)
            .parent()
            .find("[data-filter-value=" + current_filter_value + "]")
            .children();

        current_filter_elements.each( (index, iconElement )=>{
                switch (ordering_prefix) {
                    case '':
                        iconElement.className = "fas fa-random"
                break;
                    case '+':
                        iconElement.className = "fas fa-sort-alpha-asc"
                break;
                    case '-':
                        iconElement.className = "fas fa-sort-alpha-desc"
                break;
                default:
                console.error('Error: Wrong filter format.')
                }
            });

    });

}

/**
  * Create the sorting listener
  */
var createSortingListeners = function() {
    // free the old listeners
    $(".filter-dropdown-menu li").unbind();
    // create the new ones
     $(".filter-dropdown-menu li").click(function(event) {
        toggleFilter(event);
     });
}

/**
 *  Toggle data filter and set the new sort in the sorting structure
 *  @param jQueryClickEvent
 */
var toggleFilter = function(event) {
    // Stop the event propagation to avoid default behavior: close dropdown on click
    event.stopPropagation();

    var clickedButtonElementId = $(event.target).closest('li')[0];
    $('[id^="result-button-filter"]').children().attr('class','fas fa-spinner fa-spin');
    var clickedButtonValue = $(clickedButtonElementId).attr('data-filter-value');
    var tabIndex = parseFloat($(event.target) // search in the parents node the tab index
        .parent()[0]
        .closest('ul')
        .getAttribute("aria-labelledby")
        .replace("result-button-filter", ''));

    // update the sorting order in the sorting structure ( ex. ['+title', 'last_modification_date', '-template'] )
    dataSortingFields[tabIndex].forEach(function(field, index) {
        if (field.indexOf(clickedButtonValue) != -1) {

            if (field[0] === '+') {
                dataSortingFields[tabIndex][index] = '-' + field.slice(1);
            } else if (field[0] === '-') {
                dataSortingFields[tabIndex][index] = field.slice(1);
            } else {
                dataSortingFields[tabIndex][index] = '+' + field;
            }

        }
    });

    // We have updated the sorting order in the sorting structure, then we will update the GUI
    refreshFilterPanel(tabIndex);

    updateKeywordForm(cleanSortingList(dataSortingFields));
}

/**
 * Remove from the list the non sorted items ( ex. ['+a', 'b', '-c'] => ['+a', '-c'] )
 * @param {Array<Array<string>>} inputList
 * @return {Array<Array<string>>} cleaned list
 */
var cleanSortingList = function(inputList) {
    // we must work on a list copy to not alter the in memory filter state array
    var cloneInputList = JSON.parse(JSON.stringify(inputList));
    var cleanedInputList = [];
    inputList.forEach(function(itemList, inputListIndex) {
        itemList.forEach(function(item, itemIndex) {
            if (item[0] != '+' && item[0] != '-') {
                cloneInputList[inputListIndex].forEach(function(cloneItem, index) {
                    if (item == cloneItem) cloneInputList[inputListIndex].splice(index, 1);
                });
            }
        });
        cleanedInputList.push(cloneInputList[inputListIndex].join(','));
    });
    return cleanedInputList;
}