"""A task is a wrapper around a coroutine."""

class Task(object):
    """This object encapsulates a running task."""
    taskid = 0


    def __init__(self,target):
        Task.taskid += 1
        self.tid     = Task.taskid   # Task ID
        self.target  = target        # Target coroutine
        self.sendval = None          # Value to send

    
    def run(self):
        """ Run a task until it hits the next yield statement."""
        return self.target.send(self.sendval)