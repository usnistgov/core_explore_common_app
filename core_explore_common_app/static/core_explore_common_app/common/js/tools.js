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

/**
 * Get script in param thanks to its url.
 * Use a cache to avoid getting several time the same script.
 * @param url
 * @param options
 */
cachedScript = function( url, options ) {
  // Allow user to set any option except for dataType, cache, and url
  options = $.extend( options || {}, {
    dataType: "script",
    cache: true,
    url: url
  });

  // Use $.ajax() since it is more flexible than $.getScript
  // Return the jqXHR object so we can chain callbacks
  return $.ajax( options );
};