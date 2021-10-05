"""The Scheduler is the operating system."""

from queue import Queue

from pyos.systemcall import SystemCall

from .task import Task


class Scheduler(object):
    """A scheduler mimic a toy os."""

    def __init__(self):
        self.ready   = Queue()   
        self.taskmap = {}        

        # Tasks waiting for other tasks to exit
        self.exit_waiting = {}

    def new(self,target):
        """Introduce a new task to scheduler."""
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def exit(self, task):
        """Remove the task from the scheduler's task map."""
        print(f"Task {task.tid:d} terminated")
        del self.taskmap[task.tid]
        # Notify other tasks waiting for exit
        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)

    def waitforexit(self, task, waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid, []).append(task)
            return True
        else:
            return False

    def schedule(self,task):
        """Put a task onto the ready queue."""
        self.ready.put(task)

    def mainloop(self):
        """The main scheduler loop."""
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
                # if it's a SystemCall, run the system call
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            # catch task exit and cleanup
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)
