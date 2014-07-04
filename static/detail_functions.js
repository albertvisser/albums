function submitforid(value) {           // handler for the "update single track" button
    var str = document.forms["tracks"].action;
    str = str.replace('all', value);
    document.forms["tracks"].action = str;
    document.forms["tracks"].submit();
};
function reset_form() {                     // handler for the "cancel track modifications" link
    document.forms["tracks"].reset();
};
$(document).ready(function() {
    // code for adding a new track
    var has_newtrack = false;
    var newtrack = '            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
    newtrack += '          <input type="text" name="txtTrack0" size="40" maxlength="200"/>';
    newtrack += '          <input type="text" name="txtBy0" size="40" maxlength="200"/>';
    newtrack += '          <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
    newtrack += '          <textarea name="txtCred0" cols="95" rows="2"></textarea><br/>';
    // handler for adding a new track
    $('#addtrack').click(function() {
        if (has_newtrack == false)  {
            $('#submit_1').hide();
            $('#cancel_1').show();
            $('#submit_2').show();
            has_newtrack = true;
        };
        $('#newtrack').append(newtrack);
    });
    // handler for "cancel additions" button
    $('#cancel_1').click(function() {
        $('#newtrack').empty();
        has_newtrack = false;
        $('#submit_1').show();
        $('#cancel_1').hide();
        $('#submit_2').hide();
    });
    $('#cancel_1').hide();
    $('#submit_2').hide();
    // code for adding a new recording
    var has_newopname = false;
    var newopname = '            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
    newopname += '    <select name="selMed0">';
    newopname += '        <option value="0">-- type --</option>';
    newopname += '        {% for y in o_soort %}<option{%if x.type == y%} selected="selected"{%endif%}>{{y}}</option>{% endfor %}';
    newopname += '    </select>';
    newopname += '    <input type="text" name="txtOms0" size="60" maxlength="100" value="{{x.oms}}"/><br/>';
    // handler for adding a new recording
    $('#addopname').click(function() {
        if (has_newopname == false)  {
            $('#submit_3').hide();
            $('#cancel_2').show();
            $('#submit_4').show();
            has_newopname = true;
        };
        $('#newopname').append(newopname);
    });
    // handler for "cancel additions" button on recordings
    $('#cancel_2').click(function() {
        $('#newopname').empty();
        has_newopname = false;
        $('#submit_3').show();
        $('#cancel_2').hide();
        $('#submit_4').hide();
    });
    $('#cancel_2').hide();
    $('#submit_4').hide();
});
