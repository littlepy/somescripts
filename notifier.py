import pyinotify
import sqlite3
import os
from datetime import datetime


class EventHandler(pyinotify.ProcessEvent):

    def __init__(self, db_cursor):
        super(EventHandler, self).__init__()
        self.db_cursor = db_cursor

    def process_IN_CLOSE_WRITE(self, event):
        self.db_cursor.execute(
            "insert into event(event_name, path, status, create_time, finish_time) \
            values (?, ?, ?, ?, ?)",
            (event.maskname, event.pathname, 
             '0', datetime.strftime(datetime.now(), "%Y%m%d-%X"), '')
        )


#db = sqlite3.connect('file:async.db?mode=ro', uri=True)
db = sqlite3.connect('async.db', isolation_level=None)
db_cursor = db.cursor()
handler = EventHandler(db_cursor)
if os.path.exists('/var/run/pyinotify.pid'):
    os.remove('/var/run/pyinotify.pid')

mask = pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, handler)
wm.add_watch('/tmp', mask, auto_add=True, rec=True)
notifier.loop(daemonize=True, pid_file='/var/run/pyinotify.pid', stdout='/var/log/pyinotify.log')
#notifier.loop(pid_file='/var/run/pyinotify.pid', stdout='/var/log/pyinotify.log')
db.close()
notifier.stop()
