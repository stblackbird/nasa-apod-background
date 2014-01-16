desktop_nasa.py

DESCRIPTION
Gets the latest image of the day from NASA, http://apod.nasa.gov/apod/,
gets the description for that image, resize image, write description to it
and set it as the background in Gnome.

INSTALLATION
To make this work you will need to set a valid font path, a download folder
which should exist and change the resolution variables to that of your screen.
Furthermore if you want this to automatically update your desktop you should add
this script to cron jobs, or to startup applications. Also download all needed
python libraries.

ON UBUNTU JUST RUN

sudo apt-get install python-imaging

then go to
System -> Preferences -> Startup Applications
then add script like this
python /dir/to/script/desktop_nasa.x.x.py

ALSO SET VARIABLE
DOWNLOAD = '/home/stathis/.backgrounds/'
to a directory that script can use

For any suggestions, improvements, bugs feel free to contact me at
stmayridopoulos@hotmail.com

Based on a script of Christian Stefanescu, http://0chris.com

intelli_draw method from:
http://mail.python.org/pipermail/image-sig/2004-December/003064.html
