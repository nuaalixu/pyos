"""The Scheduler is the operating system."""

from queue import Queue

from .task import Task


class Scheduler(object):
    """A scheduler mimic a toy os."""

    def __init__(self):
        self.ready   = Queue()   
        self.taskmap = {}        


    def new(self,target):
        """Introduce a new task to scheduler."""
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid


    def exit(self, task):
        """Remove the task from the scheduler's task map."""
        print(f"Task {task.tid:03d} terminated")
        del self.taskmap[task.tid]


    def schedule(self,task):
        """Put a task onto the ready queue."""
        self.ready.put(task)


    def mainloop(self):
        """The main scheduler loop."""
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)
