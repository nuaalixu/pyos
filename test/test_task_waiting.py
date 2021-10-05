from pyos import Scheduler
from pyos.systemcall import NewTask, WaitTask


if __name__ == '__main__':
    def foo():
        for i in range(10):
            print(f"I'm foo, step {i}")
            yield

    def main():
        print("I'm main")
        child = yield NewTask(foo())  # launch new task
        print("Waiting for child...")
        yield WaitTask(child)  # kill the child task
        print("Child done")
        print("Main done")

    sched = Scheduler()
    sched.new(main())
    sched.mainloop()
