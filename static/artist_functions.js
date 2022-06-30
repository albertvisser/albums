function submitforid(value) { // handler for the "Wijzig" buttons on each line
    var str = document.forms["artists"].action;
    str = str.replace('all', value);
    document.forms["artists"].action = str;
    document.forms["artists"].submit();
};
function reset_form() { // handler for the "cancel all changes" button
    document.forms["artists"].reset();
};
$(document).ready(function() {
    // code for adding a new artist
    var has_newartist = false;
    var newartist = '        <div class="grid_2">';
    newartist += '            <input type="text" name="tNaam" id="tNaam0" value="" size="10" />';
    newartist += '        </div>';
    newartist += '        <div class="grid_8">';
    newartist += '            <input type="text" name="tSort" id="tSort0" value="" size="40"  />';
    newartist += '        </div>';
    newartist += '        <div class="grid_5">&nbsp;</div>';
    newartist += '        <div class="clear">&nbsp;</div>';
    // handler for adding a new artist
    $('#addartist').click(function() {
        if (has_newartist == false)  {
            $('#submit_1').hide();
            $('#cancel_1').show();
            $('#submit_2').show();
            has_newartist = true;
        };
        $('#newartist').append(newartist);
    });
    // handler for "cancel additions" button
    $('#cancel_1').click(function() {
        $('#newartist').empty();
        has_newartist = false;
        $('#submit_1').show();
        $('#cancel_1').hide();
        $('#submit_2').hide();
    });
    $('#cancel_1').hide();
    $('#submit_2').hide();
    // handler for "Filter" button
    $('#selartist').click(function() {
        var filter = $('#filter').val();
        var newurl = "/muziek/artiest/lijst/";
        if (filter != '')
            newurl += filter + '/';
        $('#allartists').attr('action', newurl);
//        $('#allartists').attr('method', 'get');
        $('#allartists').submit();
    });
});
