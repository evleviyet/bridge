"""
Task scheduler for automation processes.
"""
import time
from typing import Callable, List
import threading

class TaskScheduler:
    def __init__(self):
        self.tasks: List[Callable] = []
        self._running = False

    def add_task(self, task: Callable) -> None:
        """Add a task to the scheduler."""
        self.tasks.append(task)

    def start(self, interval: int = 300) -> None:
        """Start the scheduler."""
        self._running = True
        
        def run():
            while self._running:
                for task in self.tasks:
                    try:
                        task()
                    except Exception as e:
                        print(f"Task failed: {str(e)}")
                time.sleep(interval)
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False