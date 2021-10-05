"""This module includes kinds of system call."""

class SystemCall:
    """The base class of system call."""

    def __init__(self):
        # these attributes hold information about the environment       
        self.task = None
        self.sched = None

    def handle(self):
        pass


class GetTid(SystemCall):
    """Return a task's ID number."""

    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


class NewTask(SystemCall):
    """Create a new task."""

    def __init__(self, target):
        super().__init__()
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)


class KillTask(SystemCall):
    """Kill a task."""

    def __init__(self, tid):
        super().__init__()
        self.tid = tid
    
    def handle(self):
        task = self.sched.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)


class WaitTask(SystemCall):
    """Wait for a task to exit."""

    def __init__(self, tid):
        self.tid = tid
    
    def handle(self):
        result = self.sched.waitforexit(self.task, self.tid)
        self.task.sendval = result
        # if waiting for a non-existing task,
        # return immediately without waiting
        if not result:
            self.sched.schedule(self.task)


class ReadWait(SystemCall):
    """Wait for reading."""

    def __init__(self, f):
        super().__init__()
        self.f = f
    
    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforread(self.task, fd)


class WriteWait(SystemCall):
    """Wait for writing."""

    def __init__(self, f):
        super().__init__()
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforwrite(self.task, fd)
