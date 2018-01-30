/**
 * Get data sources results html holders
 */
var getDataSourcesResultsHTML = function(){
    var query_id = $("#query_id").html();

    $.ajax({
        url: getDataSourcesHTMLUrl,
        type : "GET",
        data: {
            'query_id': query_id
        },
        success: function(data){
            var $results = $("#results");
        	$results.html(data.results);
        	getDataSourcesResults();
        },
        error: function(data){
        }
    });
};

/**
 * Get data sources results
 */
var getDataSourcesResults = function(){
    var $results = $("#results");

    $results.find(".results-container").each(function(){
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
var getResultsPage = function(event){
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
var get_data_source_results = function(result_page, data_source_url){
    $.ajax({
        url: data_source_url,
        type : "GET",
        success: function(data){
            var nb_results_id = result_page.attr('nb_results_id');
            $("#" + nb_results_id).html(data.nb_results);
            result_page.html(data.results);
        },
        error: function(data){
            result_page.html(data.responseText);
        }
    });
};


/**
 * Shows/hides a result of the results page
 * @param event
 */
showhideResult = function(event){
	var button = event.target;
	var parent = $(event.target).parent();
	$(parent.children('.xmlResult')).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse");
	}else{
		$(button).attr("class","expand");
	}
};


/**
 * Load controllers for the results page
 */
$(document).ready(function() {
    getDataSourcesResultsHTML();
});

