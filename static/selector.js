$(document).ready(function() {
    // save the original options and their keys
    var all_opts = [];
    $('select.selartiest').children('option').each( function() {
        all_opts [ $( this ).attr('value') ] =  $( this ).html()
    });
    // initialize the search argument
    var sel = "";
    $('select.selartiest').keyup( function(event) {
        var test = event.which;       // get keycode: 48-57: 0-9; 65-90: a-z; 8 = backspace
        //~ var change = false;
        var selitem =$(this).attr('value');
        alert(sel.length+ " letters in lselection for " + $(this).attr("id") );
        if ($(this).hasClass('current') === false) { // trying to react to a possible change
            sel = "";                      //  of  selector (on start page)
            $(this).addClass('current');
        };
        // build/modify the search argument
        if (test == 8) {
            sel = sel.slice(0, -1);
            //~ change = true;
        } else if ((test >= 48 && test <=57 ) || (test >= 65 && test <= 90)) {
            sel += String.fromCharCode(test);
            //~ change = true;
        //~ } else if (test == 40) { // should change the selected value when the list is not expanded
            //~ // $( document.activeElement ).attr('value', selitem);
            //~ console.log('cursor down pressed ');
            //~ if ($( document.activeElement ) == $("me")) {
                //~ console.log('here');
            //~ };
        //~ } else if (test == 38) { // should change the selected value when the list is not expanded
            //~ console.log('cursor up pressed ' + $( document.activeElement ))
        } else {
            console.log(test)
        };
        //~ if (change == true) {
        // rebuild the select options with those containing the search argument
            $(this).empty();
            //~ $(this).append('<option value="0">-- selecteer--</option>')
            for (i in all_opts) {
                if (all_opts[i].toUpperCase().search(sel.toUpperCase()) != -1) {
                    $(this).append('<option value="' + i + '">' + all_opts[i] + "</option>");
                };
            };
            //~ $('me').attr('value', selitem);
        //~ };
    });
});
