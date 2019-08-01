$(document).ready(function () {
/* https://stackoverflow.com/a/32630356 */
window.setTimeout(function() {
    $(".alert").fadeTo(250, 0).slideUp(250, function(){
        $(this).remove(); 
    });
}, 1000);
});


/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

}())
