from watchdog.events import FileMovedEvent, FileCreatedEvent
import config
# modified_start = True

# class EventHandler(FileSystemEventHandler):
#     def on_any_event(self, event):
#         print("EVENT")
#         print(event.event_type)
#         print(event.src_path)
#         print()

    # def on_created(self, event):
    #     print("EVENT")
    #     print(event.event_type)
    #     print(event.src_path)
    #     print(event)

    # def on_moved(self, event):
    #     print("EVENT")
    #     print(event.event_type)
    #     print(event.src_path)
    #     print(event)

def on_created(event):
    # print(f"hey, {event.event_type}:{event.src_path} has been created!")
    print(f"hey, {event} has been created!")
    
    # print("FileCreatedEvent", isinstance(event, FileCreatedEvent))
    
    if isinstance(event, FileCreatedEvent):
        # print('file put waiting')
        config._queue.put(event._src_path)
    # print('all put waiting')
    # filequeue._queue.join()
    # print('put done')


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    # global modified_start
    # if modified_start:
    print(f"hey buddy, {event.src_path} has been modified")
    # else:
        # main_start = False
        # pass
    # modified_start = False
    # print("modified_start", modified_start)

def on_moved(event):
    # print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    if isinstance(event, FileMovedEvent):
        config._queue.put(event.dest_path)
    # print('put waiting')
    # filequeue._queue.join()
    # print('put done')