/** Results pages script **/

/**
 * Get data sources results html holders
 */
var getDataSourcesResultsHTML = function() {
    var query_id = $("#query_id").html();

    updateKeywordForm(dataSortingFields.split(';'));

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
        },
        error: function(data) { }
    });
};


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
        get_data_source_results(result_page, data_source_url);
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
var get_data_source_results = function(result_page, data_source_url) {

    $.ajax({
        url: data_source_url,
        type: "GET",
        success: function(data) {
            var nb_results_id = result_page.attr('nb_results_id');
            $("#" + nb_results_id).html(data.nb_results);
            result_page.html(data.results);
            // setup all the toolbar components (listeners, callbacks and default values)
            initToolbarComponents();
            // Add leave notice on links from loaded data
            leaveNotice($("#results_" + nb_results_id.match(/(\d+)/)[0] + " a"));
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
        var dataPermissionUrl = inputElement.attr("value");
        $.ajax({
            url: dataPermissionUrl,
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

    var checkboxElement = $('.switch-input');

    if (defaultDateToggleValue == 'True') {
        // set the checkbox to "checked"
        checkboxElement.prop('checked', true);
    } else {
        // set the checkbox to "unchecked"
        checkboxElement.prop('checked', false);
    }
    // create change listener
    $(".switch-input").change(function() {
        toggleDate($(this).is(":checked"));
    });

    // set the toggle to the right value one time for init
    toggleDate(checkboxElement.is(":checked"));
}

/*
 * Show / Hide the dates on the results list
 * @param: {boolean} value of the checkbox
 */
var toggleDate = function(value) {
    var dateContainers = $('.data-info-right-container');
    if(value) {
        dateContainers.show();
        $( "div[name='result']" ).addClass( "result-line-main-container" );
        $('.switch-input').prop('checked', true);
    } else {
        dateContainers.hide();
        $( "div[name='result']" ).removeClass( "result-line-main-container" );
        $('.switch-input').prop('checked', false);
    }
}


/**
 * Shows/hides a result of the results page
 * @param event
 */
showhideResult = function(event) {
    var button = event.target;
    // find the xml container
    $(event.target).parents('.result-line-main-container')
        .find(".xmlResult")
        .toggle("blind", 500);

    if ($(button).attr("class") == "expand") {
        $(button).attr("class", "collapse");
    } else {
        $(button).attr("class", "expand");
    }
};


var initToolbarComponents = function(){
    // init the sort filter when the toolbar is displayed if the script is available (sorting_multi/single_criteria.js)
    if (initFilter) initFilter();
    // when the results and the tab are displayed we can init the toggle
    initDisplayDateToggle();
    // permission api calls for the edit button
    getDataPermission();
    // listeners for the persistent query (on button_persistent_query.js)
    $(".btn-persistent-query").on('click', getPersistentUrl);
    $("#shareable-link-button").on('click', copyAndCloseModal);
}

/**
 * Load controllers for the results page
 */
$(document).ready(function() {
    getDataSourcesResultsHTML();
});