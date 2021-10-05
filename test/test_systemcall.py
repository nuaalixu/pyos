from pyos import Scheduler
from pyos.systemcall import GetTid, NewTask, KillTask


if __name__ == '__main__':
    def foo():
        mytid = yield GetTid()
        while True:
            print("I'm foo", mytid)
            yield

    def main():
        child = yield NewTask(foo())  # launch new task
        for i in range(5):
            yield
        yield KillTask(child)  # kill the child task
        print("main done")

    sched = Scheduler()
    sched.new(main())
    sched.mainloop()
