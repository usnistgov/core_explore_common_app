/**
 * Runs method once jquery is loaded
 * @param method
 */
var onjQueryReady = function(method) {
    if (window.jQuery){
        method();
    }
    else{
        setTimeout(function() { onjQueryReady(method) } , 50);
    }
};
