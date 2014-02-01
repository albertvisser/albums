======
Albums
======

is the evolution of my take on "build an application to administer your record collection".

Long ago I "inherited" my brother's old taperecorder and a collection of old tapes,
since he was kind of a sound quality buff and I guess he intended to recreate the
whole set anew, leaving out the stuff he didn't like anymore.
Along with it came a kind of notebook containing what was on the tapes.
He'd been pretty meticulous in writing down the albums, the songs on it and the
people who wrote them; and it proved to be a good basis for an attempt of my own
to make an inventory of records and recordings in my possession.

In those days (Monty Python accent) you could only buy records on vinyl,
record them on tape, and make notes on paper. So my first "system" for this
inventory was in my own handwriting, in different colours to make things more
distinguishable from each other. For the tapings (on compact cassette, later on)
I devised a way to make it possible to indicate on which tape or cassette a
specific piece of music could be found - in contrast to the earlier "list of
recordings on -this medium".

When I got my hand on computer filing programs I switched over to the digital way.
There was a nice program called RapidFile which was a cross between a spreadsheet
and a regular filing program which made it easy to enter your data and create views
on it.
Then I got a trial version of SQL/Windows which made it possible to create a layered
application from screens, logic controlling them and communicating with a separate
SQL database. I didn't quite finish it I think, but continued developing it in
Microsoft Access.

After I had discovered Python and the phenomenon of "dynamic web pages" I rebuilt
this for use on a local web server. This was with communication over simple cgi and
data storage in the form of XML files.
After somebody asked me "why don't you use a framework?" I rebuilt it in Django and
the result is this application.


Usage
-----

Use manage.py or the provided fcgi or wsgi script to start the django app, and
configure your web server to communicate with it.


Requirements
------------

- Python
- Django
- jQuery (download recent version into /static/)
