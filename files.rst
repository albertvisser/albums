
    manage.py
        standaard maintenance utility
    wsgi_handler.py
        starter om server via wsgi te gebruiken

albums\
.......

    __init__.py
        (lege) package indicator
    settings.py
        site instellingen
    urls.py
        url dispatcher
    views.py
        opbouwen van de pagina's

albums\muziek\
..............

    __init__.py
        (lege) package indicator
    admin.py
        aanmelden models op admin site
    models.py
        data mapping
    urls.py
        url dispatcher
    views.py
        opbouwen van de pagina's

albums\templates\
.................

    base.html
        algemene basis layout
    base_site.html
        site specifieke aanvullingen
    index.html
        startpagina

albums\templates\muziek\
...............................

    artiest.html
        invulsource opvoeren artiest
    artiesten.html
        invulsource lijst artiesten
    base_site.html
        basis layout subsite
    detail.html
        invulsource detailscherm
    opname.html
        invulsource wijzigen opnamegegevens
    select.html
        invulsource selectiescherm
    start.html
        invulsource startscherm
    toondetails.html
        detailscherm include
    toontracks.html
        detailscherm include
    toonopnames.html
        detailscherm include
    track.html
        invulsource wijzigen trackgegevens
    wijzigdetails.html
        detailscherm include
    wijzigtracks.html
        detailscherm include
    wijzigopnames.html
        detailscherm include

static\
.......

    admin
        symlink naar admin css

styles\
.......

    960.css
        grid-960 layout classes
    reset.css
        reset t.b.v. grid-960
    muziek.css
        site-specifieke layout
