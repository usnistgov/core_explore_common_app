/**
* Wait for Jquery to be ready
*/
var defer_initLocalProvider = function(){
    $(document).ready(function() {
        initLocalProvider();
    })
};


/**
 * Initialize the local provider
 */
var initLocalProvider = function(){
    var query_id = $("#query_id").html();
    $.ajax({
        url: getLocalDataSourceUrl,
        type : "GET",
        data: {
            query_id: query_id,
        },
        success: function(data){
            // Display federated search's data sources
            $("#list-local-data-source-content").html(data);
            // Add action on each federated search's checkbox
            var $local_selector = $("#local_selector");
            // set on change event on local selector
            $local_selector.on('change', updateLocalDataSource);
        },
        error: function(data){
        }
    });
};


/**
 * Update local data source
 */
var updateLocalDataSource = function(){
    var query_id = $("#query_id").html();
    var selected = $("#local_selector").is(":checked");
    // before every DataSource update clear the session DataSource data
    document.cookie = "selectedTabIndex=0";
    $.ajax({
        url: updateLocalDataSourceUrl,
        type : "GET",
        data: {
            'query_id': query_id,
            'selected': selected,
        },
        success: function(data){
            if(data.selected){
                var $local_selector = $("#local_selector");
                $local_selector.prop('checked', true);
            }
        },
        error: function(data){
        }
    });
};


// Waiting JQuery
onjQueryReady(defer_initLocalProvider);
