$(document).ready(function() {

    // save the original options and their keys
    var all_opts = [];
    $('#selartiest').children('option').each( function() {
        all_opts [ $( this ).attr('value') ] =  $( this ).html()
    });

    // initialize the search argument
    var sel = "", sel2 = "";
    $('#selartiest').keyup( function(event) {
        var test = event.which;
        //~ var change = false;

        // build/modify the search argument
        if (test == 8) {    // backspace
            sel = sel.slice(0, -1);
            //~ changed = true;

        } else if ((test >= 48 && test <=57 ) || (test >= 65 && test <= 90)) { // letters/digits
            sel += String.fromCharCode(test);
            //~ changed = true;
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
        //~ if (changed == true) {
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
    $('#selartiest2').keyup( function(event) {
        var test = event.which;
        //~ var change = false;

        // build/modify the search argument
        if (test == 8) {    // backspace
            sel2 = sel2.slice(0, -1);
            //~ changed = true;

        } else if ((test >= 48 && test <=57 ) || (test >= 65 && test <= 90)) { // letters/digits
            sel2 += String.fromCharCode(test);
            //~ changed = true;
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
        //~ if (changed == true) {
        // rebuild the select options with those containing the search argument
            $(this).empty();
            //~ $(this).append('<option value="0">-- selecteer--</option>')
            for (i in all_opts) {
                if (all_opts[i].toUpperCase().search(sel2.toUpperCase()) != -1) {
                    $(this).append('<option value="' + i + '">' + all_opts[i] + "</option>");
                };
            };
            //~ $('me').attr('value', selitem);
        //~ };
    });
});
