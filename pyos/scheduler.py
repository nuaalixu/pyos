"""The Scheduler is the operating system."""

from queue import Queue
import select

from pyos.systemcall import SystemCall
from .task import Task


class Scheduler(object):
    """A scheduler mimic a toy os."""

    def __init__(self):
        self.ready   = Queue()   
        self.taskmap = {}        

        # Tasks waiting for other tasks to exit
        self.exit_waiting = {}

        # I/O waiting
        self.read_waiting = {}  # holding areas of tasks blocking on I/O.
        self.write_waiting = {} # These are dictionaries mapping file descriptors to tasks.

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

    def waitforread(self, task, fd):
        """Input waiting."""
        self.read_waiting[fd] = task

    def waitforwrite(self, task, fd):
        """Output waiting."""
        self.write_waiting[fd] = task

    def iopoll(self, timeout):
        """Use select to determine which file descriptor can be used."""
        if self.read_waiting or self.write_waiting:
            r, w, e = select.select(self.read_waiting,
                                    self.write_waiting,
                                    [], timeout)
            for fd in r: self.schedule(self.read_waiting.pop(fd))
            for fd in w: self.schedule(self.write_waiting.pop(fd))

    def iotask(self):
        """wrap iopoll in a coroutine."""
        while True:
            if self.ready.empty():
                self.iopoll(None)
            else:
                self.iopoll(0)
            yield

    def schedule(self,task):
        """Put a task onto the ready queue."""
        self.ready.put(task)

    def mainloop(self):
        """The main scheduler loop."""
        self.new(self.iotask())  # launch I/O poll
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
