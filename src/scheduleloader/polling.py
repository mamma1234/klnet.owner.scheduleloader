import config
import sys
import time
import logging
from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
# from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
from pathlib import Path
import os
import event
import shutil


# class EventHandler(FileSystemEventHandler):
#     def on_any_event(self, event):
#         print("EVENT")
#         print(event.event_type)
#         print(event.src_path)
#         print(event)


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')
# path = sys.argv[1] if len(sys.argv) > 1 else '.'
# event_handler = LoggingEventHandler()

def work():
    # event_handler = EventHandler()
    # main_start = True
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    event_handler.on_created = event.on_created
    # event_handler.on_deleted = event.on_deleted
    # event_handler.on_modified = event.on_modified
    event_handler.on_moved = event.on_moved
    observer = Observer()
    observer.schedule(event_handler, config._path, recursive=True)
    observer.start()

    # print("path",path)
    # for root, dirs, files in os.walk(path):
    copypaths = []
    for dir in os.listdir(config._path):
        # print("dir", dir)
        # abspath = os.path.abspath(dir)
        # print("abspath", abspath)
        subdir = config._path +"/" + dir
        subfiles = os.listdir(config._path +"/" + dir)
        if len(subfiles) > 0:
            copypaths.append(subdir)
    
    # print(copypaths)
    if len(copypaths) > 0:
        for copypath in copypaths:
            # print("copy:", copypath)
            # shutil.copytree(copypath, f"{copypath}-Copy")
            shutil.move(copypath, f"{copypath}-Copy")
        # if os.path.isfile(path):
        #     copypath.append(path)
# os.path.isfile(path)
        # print(os.path.isfile(path + '\\' + dir))

            # shutil.copytree(dir, f"{dir}-Copy")

    #         for file in files:
    #             # print(file)
    #             Path(os.path.join(root, file)).touch()
    # main_start = False

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()