import sys
import time
import logging
from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler

from pathlib import Path
import os

path = "C:\\KLNET\\SCH"

def on_created(event):
    print(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")

def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
"""
class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        print("EVENT")
        print(event.event_type)
        print(event.src_path)
        print(event)
"""
"""
    def on_any_event(self, event):
        print("EVENT")
        print(event.event_type)
        print(event.src_path)
        print(event)
"""

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')
# path = sys.argv[1] if len(sys.argv) > 1 else '.'
# event_handler = LoggingEventHandler()



# event_handler = EventHandler()
main_start = True
patterns = "*"
ignore_patterns = ""
ignore_directories = False
case_sensitive = True
event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

event_handler.on_created = on_created
event_handler.on_deleted = on_deleted
event_handler.on_modified = on_modified
event_handler.on_moved = on_moved
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

if main_start:
    for root, dirs, files in os.walk(path):
        for file in files:
            # print(file)
            Path(os.path.join(root, file)).touch()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()