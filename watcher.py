# Script for watching the downloads folder and automatically runs when something is added to the file
import time
import argparse
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import threading
from Sorter import organize_files
import json

WATCHED_DIR = str(Path.home() / "Downloads")
IGNORED_EXTENSIONS = {'.crdownload', '.part', '.tmp', '.partial'}

DEBOUNCE_DELAY = 5  # seconds

class DebouncedHandler(FileSystemEventHandler):
    def __init__(self, delay, ignore_exts, organize_func):
        self.delay = delay
        self.timer = None
        self.ignore_exts = set(ignore_exts)
        self.organize_func = organize_func

    def on_any_event(self, event):
        # Ignore directories
        print(f"Detected event: {event}")
        if event.is_directory:
            return
        
        # Ignore files with ignored extensions
        if any(event.src_path.endswith(ext) for ext in self.ignore_exts):
            print(f"Ignored change on {event.src_path}")
            return
        
        # Reset debounce timer on every event
        if self.timer:
            self.timer.cancel()

        self.timer = threading.Timer(self.delay, self.run_organize)
        self.timer.start()

    def run_organize(self):
        print(f"No changes for {self.delay} seconds, running organize function...")
        self.organize_func()

def load_rules(path='file_rules.json'):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Watch folder and run organize_files on changes.")
    parser.add_argument('--auto-run', action='store_true', help='Automatically run organize_files on file changes')
    parser.add_argument('--ignore-ext', nargs='*', default=[], help='List of file extensions to ignore, e.g. .tmp .json')
    parser.add_argument('--path', default=str(Path.home() / "Downloads"), help='Path to watch, default is Downloads folder')
    parser.add_argument("--rules", default="file_rules.json", help="Path to the rules config file.")
    args = parser.parse_args()

    if not args.auto_run:
        user_choice = input("Run organize_files on changes? (y/n): ").strip().lower()
        if user_choice != 'y':
            print("Auto-run disabled. Exiting.")
            return

    # Default ignored extensions (you can customize this)
    default_ignored = {'.json', '.tmp', '.log'}
    # Combine with user-provided extensions
    ignored_exts = default_ignored.union(set(args.ignore_ext))

    print(f"Watching path: {args.path}")
    print(f"Ignoring extensions: {ignored_exts}")
    print("Waiting for file changes...")

   #event_handler = DebouncedHandler(delay=5, ignore_exts=ignored_exts, organize_func=organize_files)
    event_handler = DebouncedHandler(
        delay=5,
        ignore_exts=ignored_exts,
        organize_func=lambda: organize_files(args.path, load_rules(args.rules), recursive=True)
    )


    observer = Observer()
    observer.schedule(event_handler, args.path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observer...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
