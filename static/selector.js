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
        var changed = false;

        // build/modify the search argument
        if (test == 8) {    // backspace
            sel = sel.slice(0, -1);
            changed = true;
        } else if ((test >= 48 && test <=57 ) || (test >= 65 && test <= 90)) { // letters/digits
            sel += String.fromCharCode(test);
            changed = true;
        };

        if (changed == true) {
            // rebuild the select options with those containing the search argument
            $(this).empty();
            for (i in all_opts) {
                if (all_opts[i].toUpperCase().search(sel.toUpperCase()) != -1) {
                    $(this).append('<option value="' + i + '">' + all_opts[i] + "</option>");
                };
            };
        };
    });

    $('#selartiest2').keyup( function(event) {
        var test = event.which;
        var changed = false;

        // build/modify the search argument
        if (test == 8) {    // backspace
            sel2 = sel2.slice(0, -1);
            changed = true;
        } else if ((test >= 48 && test <=57 ) || (test >= 65 && test <= 90)) { // letters/digits
            sel2 += String.fromCharCode(test);
            changed = true;
        };

        if (changed == true) {
        // rebuild the select options with those containing the search argument
            $(this).empty();
            for (i in all_opts) {
                if (all_opts[i].toUpperCase().search(sel2.toUpperCase()) != -1) {
                    $(this).append('<option value="' + i + '">' + all_opts[i] + "</option>");
                };
            };
        };
    });

});
