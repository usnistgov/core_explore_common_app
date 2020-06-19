/**
 * Load controllers for the persistent query button
 */
$(document).ready(function() {
    initSharingModal(
        configurePersistentQueryModal, "#persistent-query", "#persistent-query-modal",
        "#persistent-query-link", "#persistent-query-submit"
    );
});

let configurePersistentQueryModal = function() {
    // Check the persistent query url has been defined.
    if (typeof persistentQueryUrl === "undefined" || persistentQueryUrl === null) {
        showErrorModal("No persistent query URL defined");
        return false;
    }

    let hasFailed = false;
    let queryId = $("#query_id").html();

    $.ajax({
        url: persistentQueryUrl,
        data: { queryId },
        type: "POST",
        dataType: "json",
        async: false,
        success: function(data){
            $("#persistent-query-link").val(data.url);
        },
        error:function(){
            showErrorModal("Error while retrieving persistent query.");
            hasFailed = true;
        }
    });

    return !hasFailed;
}