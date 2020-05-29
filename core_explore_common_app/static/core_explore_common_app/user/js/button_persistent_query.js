/**
* Persistent query button manager
*/

getPersistentUrl = function(event){
    /**
     * Generate persistent query URL by performing an Ajax call on a pre-defined URL.
     */
    event.preventDefault();

    // Check the persistent query url has been defined.
    if (typeof persistentQueryUrl === "undefined" || persistentQueryUrl === null) {
        showErrorModal("No persistent query URL defined");
    }

    let queryId = $("#query_id").html();

    $.ajax({
        url: persistentQueryUrl,
        data: { queryId },
        type: "POST",
        dataType: "json",
        success: function(data){
            $("#shareable-link").val(data.url);
            $("#persistent-query-modal").modal("show");
        },
        error:function(){
            showErrorModal("Error while retrieving persistent query.");
        }
    });
};

copyAndCloseModal = function(event){
    /**
     * Copy the link on clipboard and close the modal
     */
    event.preventDefault();

    let link = $("#shareable-link");
    link.prop('disabled', false);
    link.focus();
    link.select();
    document.execCommand('copy');
    link.prop('disabled', true);

    $("#persistent-query-modal").modal("hide");
};