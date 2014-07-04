    $('#selartist').click(function() {
        var dest = "/muziek/artiest/lijst/"
        var filter = $('#filter').val();
        if (filter != "")
            dest += filter + '/';
        document.location=dest;
    });
