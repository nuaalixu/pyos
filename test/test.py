from pyos import Scheduler


if __name__ == '__main__':
    def foo():
        for i in range(10):
            print("I'm foo")
            yield

    def bar():
        for i in range(5):
            print("I'm bar")
            yield

    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()
