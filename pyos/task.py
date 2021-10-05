"""A task is a wrapper around a coroutine."""
from typing import Generator

from pyos.systemcall import SystemCall


class Task(object):
    """This object encapsulates a running task."""
    taskid = 0


    def __init__(self,target):
        Task.taskid += 1
        self.tid     = Task.taskid   # Task ID
        self.target  = target        # Target coroutine
        self.sendval = None          # Value to send
        self.stack   = []            # Call stack

    
    def run(self):
        """ Run a task until it hits the next yield statement."""
        while True:
            try:
                result = self.target.send(self.sendval)
                # if it's a systemcall, just return
                if isinstance(result, SystemCall): return result
                # if it's a generator, we're going to "trampoline"
                if isinstance(result, Generator):
                    self.stack.append(self.target)
                    self.sendval = None
                    self.target = result
                # if some other value is combing back, assume it's a return value from a subroutine
                else:
                    if not self.stack: return
                    self.sendval = result
                    self.target = self.stack.pop()
            # if subroutines terminate, pop the last coroutine off the stack or kill the whole task
            except StopIteration:
                if not self.stack: raise
                self.sendval = None
                self.target = self.stack.pop()
