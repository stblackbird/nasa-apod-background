# Set DBUS_SESSION_BUS_ADDRESS
# Taken from http://askubuntu.com/questions/140305/cron-not-able-to-succesfully-change-background
PID=$(pgrep gnome-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)

# Run the script
python /full/path/to/script/desktop_nasa.py
