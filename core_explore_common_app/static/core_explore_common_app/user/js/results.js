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
            // setup all the toolbar components (listeners, callbacks and default values)
            initToolbarComponents();
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
            // display the date
            initDisplayDateToggle();
            // permission api calls for the edit button
            getDataPermission();
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
                            (function () {
                                var target_id = id;
                                $(editLinkElement).click(function() {
                                  openEditRecord(target_id);
                                });
                            }());
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
    var match = document.cookie.match(new RegExp('(^| )dateToggleValue=([^;]+)'));
    var toggleValue
    if (match && match.length > 1) {
        toggleValue = match[2] == 'true' ? true : false;
    } else {
        toggleValue = defaultDateToggleValue == 'True' ? true : false;
        document.cookie = "dateToggleValue=" + toggleValue;
    }

    var checkboxElement = $('.switch-input');

    if (toggleValue) {
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
        $('.switch-input').prop('checked', true);
    } else {
        dateContainers.hide();
        $('.switch-input').prop('checked', false);
    }
    // update the cookie with the new toggle date value
    document.cookie = "dateToggleValue=" + value;
};


/**
 * Shows/hides a result of the results page
 * @param event
 */
showhideResult = function(event) {
    let button = event.target;
    // find the xml container
    $(button).parents('.result-line-main-container')
        .find(".xmlResult")
        .toggle("blind", 500);

    if ($(button).attr("class") === "expand") {
        $(button).attr("class", "collapse show");
    } else {
        $(button).attr("class", "expand");
    }
};


var initToolbarComponents = function(){
    // init the sort filter when the toolbar is displayed if the script is available (sorting_multi/single_criteria.js)
    if (typeof initFilter === "function") initFilter();
    // init the autosubmit for the sorting button if available
    if (typeof initSortingAutoSubmit === "function") initSortingAutoSubmit();
    // add Tab state listener
    initTabStateListener();
    // enable the tool-bar buttons after the end of the toolbar initialization
    $(".result-toolbar-button").attr("disabled", false);
};

/**
 * Add the click listeners on the tabs to store their state in the session
 */
var initTabStateListener = function() {
    // add a listener to the tab to store their states
    var jqPresentationElement = $("li[role=presentation]");
    var jqDataSourceCheckboxElement = $(".tab-selector input:checkbox");
    jqPresentationElement.unbind( "click" );
    jqDataSourceCheckboxElement.off( "click", resetDataSourceCookie );

    // when the user click on one tab set this tab as current tab on the session data
    jqPresentationElement.on("click", function(event) {
        document.cookie = "selectedTabIndex=" + $("li[role=presentation]").index(this);
    });
    // before every DataSource update clear the session DataSource data
    jqDataSourceCheckboxElement.on("click", resetDataSourceCookie);


    // select the correct tab
    var tabSessionIndex = document.cookie.match(new RegExp("(^| )selectedTabIndex=([^;]+)"));
    if (tabSessionIndex && tabSessionIndex.length > 1) {
        // if the tab exist get the index otherwise use the default tab
        var selectedTabValue = $("#results_" + tabSessionIndex[2]).length > 0 ? tabSessionIndex[2] : 0;
        // activate the right tab according to the index
        $(jqPresentationElement[selectedTabValue]).find('.nav-link').tab('show');
        $("div[id^='results_']").removeClass('active');
        $("#results_" + selectedTabValue).addClass('active');
    }

}

/**
  * Reset the dataSource cookie to it default value
  */
var resetDataSourceCookie = function(event) {
        document.cookie = "selectedTabIndex=0";
}

/**
 * Load controllers for the results page
 */
$(document).ready(function() {
    getDataSourcesResultsHTML();
});