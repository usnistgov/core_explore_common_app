/*
* button persistent query js file
*/

/**
 * AJAX call, get persistent Url with the hidden url
 */
getPersistentUrl = function(event){
    event.preventDefault();

    // find the target's toolbar, and then find the URL
    var url = $(event.target)
        .parents(".result-toolbar")
        .find(".persistent-url-link")
        .attr("href");

    var queryId = $("#query_id").html();

    $.ajax({
        url: url,
        data: { queryId },
        type: "POST",
        dataType: "json",
        success: function(data){
            $("#shareable-link").val(data.url);
            $("#persistent-query-modal").modal("show");
        },
        error:function(data){
            alert("fail");
        }
    });
};

/**
 * Copy the link and close the modal
 */
copyAndCloseModal = function(event){
    event.preventDefault();
    var link = $("#shareable-link");
    link.prop('disabled', false);
    link.focus();
    link.select();
    document.execCommand('copy');
    link.prop('disabled', true);
    $("#persistent-query-modal").modal("hide");
}