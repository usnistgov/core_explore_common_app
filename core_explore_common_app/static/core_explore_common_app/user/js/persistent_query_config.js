/**
 * Load controllers for the persistent query button
 */
$(document).ready(function() {
    // Check the persistent query url has been defined.
    if (typeof persistentQueryUrl === "undefined" || persistentQueryUrl === null) {
        showErrorModal("No persistent query URL defined");
        return;
    }

    let queryId = $("#query_id").html();

    $.ajax({
        url: persistentQueryUrl,
        data: { queryId },
        type: "POST",
        dataType: "json",
        success: function(data){
            initSharingModal(
                data.url, "#persistent-query", "#persistent-query-modal",
                "#persistent-query-link", "#persistent-query-submit"
            );
        },
        error:function(){
            showErrorModal("Error while retrieving persistent query.");
        }
    });
});