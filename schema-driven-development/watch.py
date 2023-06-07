import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s'
    )


class BuildHandler(FileSystemEventHandler):
    def on_modified(self, event):
        super().on_modified(event)

        if not event.is_directory:
            subprocess.run(["python", "build.py", event.src_path])


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else './src'
    event_handler = BuildHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
