/**
 * Load controllers for the persistent query button
 */
let persistent_query_id = ""
$(document).ready(function() {
    initSharingModal(
        configurePersistentQueryModal, "#persistent-query", "#persistent-query-modal",
        "#persistent-query-link", "#persistent-query-submit"

    );
    $('#persistent-query-name').on('input',changeRenameButtonVisibility);
    $('#persistent-query-rename').click(renamePersistentQuery);
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
            persistent_query_id = ""
        },
        error:function(){
            showErrorModal("Error while retrieving persistent query.");
            hasFailed = true;
        }
    });
    return !hasFailed;
}


let renamePersistentQuery = function(e){
    $("#banner_set_name_query_errors").hide();

    var persistent_query_name = $("#persistent-query-name").val()
    var persistent_query_url = $("#persistent-query-link").val()

    // get persistent query id if not set
    if (persistent_query_id == "") persistent_query_id = persistent_query_url.split("=")[1]

    $.ajax({
        url: persistentQueryRestUrl.replace("queryId", persistent_query_id),
        data: { "name": persistent_query_name },
        dataType:"json",
        type: "patch",
        success: function(data){
            // update the link input
            $("#persistent-query-link").val(persistent_query_url.split("?")[0]+"?name="+persistent_query_name);

            // clear the name input
            $("#persistent-query-name").val("")

            // enable the rename button
            $('#persistent-query-rename').prop('disabled', true);



        },
        error: function(data){
             $("#set_name_query_errors").html(JSON.parse(data.responseText).message.name);
             $("#banner_set_name_query_errors").show(500)
        }
    });
 }

let changeRenameButtonVisibility = function(e){
   if( $("#persistent-query-name").val() != '') {
       $('#persistent-query-rename').prop('disabled', false);
   }
   else{
      $('#persistent-query-rename').prop('disabled', true);
   }
}
