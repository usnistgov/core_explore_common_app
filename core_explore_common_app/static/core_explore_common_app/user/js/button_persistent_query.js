/*
* button persistent query js file
*/

$(document).ready(function() {
    $("#btn-persistent-query").on('click', getPersistentUrl);
    $("#shareable-link-button").on('click', copyAndCloseModal);
})

/**
 * AJAX call, get persistent Url with the hidden url
 */
getPersistentUrl = function(event){
    event.preventDefault();

    var url = $("#btn-persistent-query").attr('href');
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